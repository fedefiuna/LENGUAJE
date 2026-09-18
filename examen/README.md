# API - Planta Industrial

**Materia:** Lenguajes de Programación Visual  
**Facultad:** Facultad de Ingeniería - UNA  
**Alumno:** Federico Da Silva  

---

## Descripción
API REST desarrollada con FastAPI, SQLAlchemy y Pydantic para la ingesta, persistencia y análisis estadístico proveniente de nodos sensores industriales.

---

## Instalación

1. Asegúrate de tener instalado **Python 3.10+** y **Poetry**.
2. Instala las dependencias del proyecto desde la raíz:

```cmd
poetry install
poetry install
poetry run uvicorn src.main:examen --reload
py simulador.py http://localhost:8000
