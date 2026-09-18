from pydantic import BaseModel
from typing import Optional

# Sensores
class SensorBase(BaseModel):
    nodo: str
    tipo: str
    modelo: str
    unidad: str
    rango_max: float

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        from_attributes = True


#Lecturas
class LecturaBase(BaseModel):
    sensor_id: int
    valor: float
    timestamp: str

class LecturaCreate(LecturaBase):
    pass

class LecturaUpdate(BaseModel):
    valor: float

class LecturaResponse(LecturaBase):
    id: int

    class Config:
        from_attributes = True

#Calculos
class EstadisticaResponse(BaseModel):
    sensor_id: int
    minimo: float
    maximo: float
    promedio: float