from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from examen.database import get_db
from examen.models import SensorDB
from examen.schemas import SensorCreate, SensorResponse

router = APIRouter(prefix="/api/sensores", tags=["Sensores"])

@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    nuevo_sensor= SensorDB(**sensor.model_dump())
    db.add(nuevo_sensor)
    db.commit()
    db.refresh(nuevo_sensor)
    return nuevo_sensor

@router.get("", response_model=List[SensorResponse])
def get_sensores(db: Session = Depends(get_db)):
    sensores = db.query(SensorDB).all()
    return sensores

@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = db.query(SensorDB).filter(SensorDB.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor no encontrado")
    db.delete(sensor)
    db.commit()
    return None