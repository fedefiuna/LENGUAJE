from fastapi import APIRouter, Depends,HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from examen.database import get_db
from examen.models import LecturaDB, SensorDB
from examen.schemas import LecturaCreate, LecturaResponse, LecturaUpdate ,EstadisticaResponse

router = APIRouter(prefix="/api/lecturas", tags=["Lecturas"])

@router.post("", response_model=LecturaResponse, status_code=status.HTTP_201_CREATED)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    sensor = db.query(SensorDB).filter(SensorDB.id == lectura.sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    nueva_lectura = LecturaDB(**lectura.model_dump())
    db.add(nueva_lectura)
    db.commit()
    db.refresh(nueva_lectura)
    return nueva_lectura


@router.get("", response_model=List[LecturaResponse])
def historial_lecturas(sensor_id: Optional[int] = Query(None), limit: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(LecturaDB)
    if sensor_id is not None:
        query = query.filter(LecturaDB.sensor_id == sensor_id)
    lecturas = query.all()
    return lecturas


@router.get("/estadisticas/{sensor_id}", response_model=EstadisticaResponse)
def obtener_estadisticas(sensor_id: str, db: Session = Depends(get_db)):
    sensor = db.query(SensorDB).filter(SensorDB.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    
    stats = db.query(
        func.min(LecturaDB.valor).label("minimo"),
        func.max(LecturaDB.valor).label("maximo"),
        func.avg(LecturaDB.valor).label("promedio")
    ).filter(LecturaDB.sensor_id == sensor_id).first()

    return {
        "sensor_id":sensor_id,
        "minimo":round(stats.minimo, 2) if stats.minimo is not None else 0.0,
        "maximo":round(stats.maximo, 2) if stats.maximo is not None else 0.0,
        "promedio":round(stats.promedio, 2) if stats.promedio is not None else 0.0
    }

@router.put("/{lectura_id}", response_model=LecturaResponse)
def corregir_lectura(lectura_id: int, lectura_data: LecturaUpdate, db: Session = Depends(get_db)):
    lectura = db.query(LecturaDB).filter(LecturaDB.id == lectura_id).first()
    if not lectura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada")
    lectura.valor = lectura_data.valor
    db.commit()
    db.refresh(lectura)
    return lectura

@router.delete("/{lectura_id}", status_code=status.HTTP_204_NO_CONTENT)
def depurar_lectura(lectura_id: int, db: Session = Depends(get_db)):
    lectura = db.query(LecturaDB).filter(LecturaDB.id == lectura_id).first()
    if not lectura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada")
    db.delete(lectura)
    db.commit()
    return None
