import os
from dotenv import load_dotenv
from extract import fetch_all_cities
from transform import transform_weather, validate
from load import get_engine, create_table, load_to_db

load_dotenv()

def run():
    print("=== Démarrage du pipeline météo ===")

    # 1. Extract
    cities = os.getenv("CITIES", "Tunis").split(",")
    raw = fetch_all_cities(cities)
    if not raw:
        print("Aucune donnée récupérée, arrêt.")
        return

    # 2. Transform
    df = transform_weather(raw)
    df = validate(df)
    print(f"→ {len(df)} enregistrements après transformation")

    # 3. Load
    engine = get_engine()
    create_table(engine)
    load_to_db(df, engine)

    print("=== Pipeline terminé avec succès ===")

if __name__ == "__main__":
    run()