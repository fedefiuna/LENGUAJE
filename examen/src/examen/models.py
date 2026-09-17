from sqlalchemy import Column, Integer, String, Float,ForeignKey
from examen.database import Base


class SensorDB(Base):
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True)
    nodo = Column(String, index=True, nullable=False)
    tipo = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    unidad = Column(String, nullable=False)
    rango_max = Column(Float, nullable=False)


class LecturaDB(Base):
    __tablename__ = "lecturas"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensores.id"), nullable=False)
    valor = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
