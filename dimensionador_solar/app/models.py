from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class PanelSolar(Base):
    __tablename__ = "paneles_solares"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    marca: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    potencia_pico_wp: Mapped[float] = mapped_column(Float, nullable=False)
    eficiencia_porcentaje: Mapped[float] = mapped_column(Float, nullable=False)
    voltaje_voc: Mapped[float] = mapped_column(Float, nullable=False)
    coeficiente_temp: Mapped[float] = mapped_column(Float, nullable=False)


class Inversor(Base):
    __tablename__ = "inversores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    marca: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    modelo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    potencia_nominal_w: Mapped[float] = mapped_column(Float, nullable=False)
    rango_mppt_min: Mapped[float] = mapped_column(Float, nullable=False)
    rango_mppt_max: Mapped[float] = mapped_column(Float, nullable=False)