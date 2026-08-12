import os
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(url)

def create_table(engine):
    """Crée la table si elle n'existe pas encore."""
    ddl = """
    CREATE TABLE IF NOT EXISTS weather_readings (
        id          SERIAL PRIMARY KEY,
        city        TEXT NOT NULL,
        country     TEXT,
        temperature NUMERIC(5,2),
        feels_like  NUMERIC(5,2),
        temp_min    NUMERIC(5,2),
        temp_max    NUMERIC(5,2),
        humidity    INTEGER,
        pressure    INTEGER,
        wind_speed  NUMERIC(6,2),
        wind_deg    INTEGER,
        description TEXT,
        icon        TEXT,
        visibility  NUMERIC(6,2),
        clouds      INTEGER,
        fetched_at  TIMESTAMPTZ NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_city_time
        ON weather_readings (city, fetched_at DESC);
    """
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()

def load_to_db(df: pd.DataFrame, engine) -> int:
    """Insère le DataFrame dans PostgreSQL. Retourne le nombre de lignes insérées."""
    rows = df.to_sql(
        name="weather_readings",
        con=engine,
        if_exists="append",   # ajoute sans écraser les données existantes
        index=False,
    )
    print(f"✓ {rows} lignes insérées dans la base")
    return rows