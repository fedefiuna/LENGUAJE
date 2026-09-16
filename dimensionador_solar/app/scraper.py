import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# 1. Función para obtener radiación solar en tiempo real (Open-Meteo API)
async def obtener_radiacion_solar(latitud: float, longitud: float) -> float:
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitud}&longitude={longitud}&daily=shortwave_radiation_sum&timezone=auto"
    )
    
    async with httpx.AsyncClient() as client:
        respuesta = await client.get(url)
        datos = respuesta.json()
        
        # Obtenemos la radiación solar diaria en MJ/m²
        radiaciones_mj = datos["daily"]["shortwave_radiation_sum"]
        
        # Convertimos el promedio de MJ/m² a kWh/m²/día (1 MJ = 0.277778 kWh)
        promedio_mj = sum(radiaciones_mj) / len(radiaciones_mj)
        promedio_kwh_m2 = promedio_mj * 0.277778
        
        return round(promedio_kwh_m2, 2)

# 2. Extracción asíncrona de catálogo de equipos
async def extraer_catalogo_equipos() -> Dict[str, List[Dict[str, Any]]]:
    # Simulamos el scraping asíncrono a una fuente técnica web externa con HTTPX
    async with httpx.AsyncClient() as client:
        # Aquí consumirías la URL real de un catálogo HTML o JSON
        paneles = [
            {"marca": "Jinko Solar", "modelo": "Tiger Pro 540W", "potencia_pico_wp": 540.0, "eficiencia_porcentaje": 20.9, "voltaje_voc": 49.5, "coeficiente_temp": -0.35},
            {"marca": "Canadian Solar", "modelo": "HiKu6 550W", "potencia_pico_wp": 550.0, "eficiencia_porcentaje": 21.3, "voltaje_voc": 49.6, "coeficiente_temp": -0.34},
            {"marca": "LONGi Solar", "modelo": "LR5-72HPH 545W", "potencia_pico_wp": 545.0, "eficiencia_porcentaje": 21.1, "voltaje_voc": 49.65, "coeficiente_temp": -0.35},
        ]
        
        inversores = [
            {"marca": "Fronius", "modelo": "Primo 5.0-1", "potencia_nominal_w": 5000.0, "rango_mppt_min": 80.0, "rango_mppt_max": 1000.0},
            {"marca": "Huawei", "modelo": "SUN2000-6KTL-L1", "potencia_nominal_w": 6000.0, "rango_mppt_min": 90.0, "rango_mppt_max": 560.0},
            {"marca": "Growatt", "modelo": "MIN 3000TL-X", "potencia_nominal_w": 3000.0, "rango_mppt_min": 80.0, "rango_mppt_max": 550.0},
        ]
        
    return {"paneles": paneles, "inversores": inversores}