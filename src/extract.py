import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str) -> dict:
    """Récupère les données météo brutes pour une ville."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Celsius
        "lang": "fr",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()  # Lève une erreur si le code HTTP n'est pas 200
    return response.json()

def fetch_all_cities(cities: list[str]) -> list[dict]:
    """Récupère les données pour toutes les villes."""
    results = []
    for city in cities:
        try:
            data = fetch_weather(city)
            results.append(data)
            print(f"✓ {city} récupéré")
        except requests.RequestException as e:
            print(f"✗ Erreur pour {city}: {e}")
    return results