from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

#URL de la base de datos SQLite con driver asincrono
DATABASE_URL = "sqlite+aiosqlite:///./solar_app.db"

# Creacion del motor asincrono
engine = create_async_engine(DATABASE_URL, echo=True)

#Generador de sesiones asincronas para las rutas del FastAPI
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#Clase base para la creacion de los modelos
class Base(DeclarativeBase):
    pass

#Dependencia para inyectar la sesion de BD en FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session