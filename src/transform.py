import pandas as pd
from datetime import datetime, timezone

def transform_weather(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transforme les JSON bruts de l'API en DataFrame propre.
    Extrait seulement les champs utiles, renomme, convertit les types.
    """
    records = []

    for item in raw_data:
        record = {
            "city":          item["name"],
            "country":       item["sys"]["country"],
            "temperature":   item["main"]["temp"],        # °C
            "feels_like":    item["main"]["feels_like"],  # °C
            "temp_min":      item["main"]["temp_min"],
            "temp_max":      item["main"]["temp_max"],
            "humidity":      item["main"]["humidity"],    # %
            "pressure":      item["main"]["pressure"],    # hPa
            "wind_speed":    item["wind"]["speed"],       # m/s
            "wind_deg":      item["wind"].get("deg", 0),
            "description":   item["weather"][0]["description"],
            "icon":          item["weather"][0]["icon"],
            "visibility":    item.get("visibility", 0) / 1000,  # km
            "clouds":        item["clouds"]["all"],              # %
            "fetched_at":    datetime.now(timezone.utc),        # timestamp UTC
        }
        records.append(record)

    df = pd.DataFrame(records)

    # Conversions de types
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])
    df["humidity"]   = df["humidity"].astype(int)
    df["pressure"]   = df["pressure"].astype(int)
    df["clouds"]     = df["clouds"].astype(int)

    return df

def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre les lignes corrompues ou hors limites physiques."""
    df = df.dropna(subset=["city", "temperature"])
    df = df[df["temperature"].between(-80, 60)]   # températures impossibles
    df = df[df["humidity"].between(0, 100)]
    return df