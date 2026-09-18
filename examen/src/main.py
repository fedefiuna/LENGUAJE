from fastapi    import FastAPI
from examen.database import engine, Base
from examen.routers  import sensores , lecturas


Base.metadata.create_all(bind=engine)

examen=FastAPI(title="Parcial", description="API REST de planta")

examen.include_router(sensores.router)
examen.include_router(lecturas.router)
