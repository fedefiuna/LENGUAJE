from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from math import ceil

from app.database import engine, Base, get_db
from app.models import PanelSolar, Inversor
from app.scraper import extraer_catalogo_equipos, obtener_radiacion_solar

#Evento para inicializar las tablas SQLite en el arranque
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Dimensionador Solar Fotovoltaico API", lifespan=lifespan)

#Endpoint 1: Poblar base de datos usando el scraper en segundo plano
@app.post("/poblar-catalogo")
async def poblar_catalogo(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    equipos = await extraer_catalogo_equipos()

#guardar paneles 
    for p in equipos["paneles"]:
        stmt = select(PanelSolar).where(PanelSolar.modelo == p["modelo"])
        res=await db.execute(stmt)
        if not res.scalar_one_or_none():
            db.add(PanelSolar(**p))

    await db.commit()
    return {"mensaje": "Catálogo de equipos actualizado"}

#Endpoint 2: Dimensionamiento Fotovoltaico interactivo
@app.post("/dimensionar")
async def dimensionar_sistema(
    latitud: float,
    longitud: float,
    consumo_diario_kwh: float,
    db: AsyncSession = Depends(get_db)
):
    #Peticion asincona a la API de Radiacion Solar
    hps=await obtener_radiacion_solar(latitud, longitud)
    if hps <= 0:
        raise HTTPException(status_code=400, detail="Radiación solar no disponible para la ubicación proporcionada.")

    #Seleccion del panel solar con mayor potencia desde SQLite
    stmt_panel = select(PanelSolar).order_by(PanelSolar.potencia_pico_wp.desc())
    panel_optimo = (await db.execute(stmt_panel)).scalars().first() 

    if not panel_optimo:
        raise HTTPException(status_code=404, detail="No se encontraron paneles solares en la base de datos.")

    #Calculo matematico del req
    energia_objetivo_kwh = consumo_diario_kwh *1.2
    potencia_matriz_kwp = energia_objetivo_kwh / hps


    potencia_panel_kwp = panel_optimo.potencia_pico_wp / 1000
    num_paneles = ceil(potencia_matriz_kwp / potencia_panel_kwp)
    potencia_instalada_kwp = round(num_paneles * potencia_panel_kwp, 2) 

    #Seleccion del inversor adecuado en SQLite
    stmt_inversor = select(Inversor).where(Inversor.potencia_nominal_w >= potencia_instalada_kwp * 1000).order_by(Inversor.potencia_nominal_w.asc())
    inversor_optimo = (await db.execute(stmt_inversor)).scalars().first()

    return { 
        "ubicacion": {"latitud": latitud, "longitud": longitud},
        "radiacion_solar_kwh_m2_dia": hps,
        "consumo_diario_kwh": consumo_diario_kwh,
        "dimensionamiento" : {
            "panel_optimo": f"{panel_optimo.marca} {panel_optimo.modelo}",
            "num_paneles": num_paneles,
            "potencia_instalada_kwp": potencia_instalada_kwp,
            "inversor_optimo": f"{inversor_optimo.marca} {inversor_optimo.modelo}" if inversor_optimo else "No se encontró un inversor adecuado"
        }

        }
