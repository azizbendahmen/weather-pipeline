import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Météo Pipeline", page_icon="🌤", layout="wide")

@st.cache_resource
def get_engine():
    url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(url)

@st.cache_data(ttl=300)  # rafraîchit le cache toutes les 5 minutes
def load_data():
    engine = get_engine()
    query = """
        SELECT * FROM weather_readings
        ORDER BY fetched_at DESC
        LIMIT 5000
    """
    return pd.read_sql(query, engine)

# --- UI ---
st.title("🌤 Weather Data Pipeline")
st.caption("Données rafraîchies toutes les heures · PostgreSQL + Streamlit")

df = load_data()

if df.empty:
    st.warning("Aucune donnée. Lance d'abord le pipeline : `python src/pipeline.py`")
    st.stop()

# Filtres sidebar
cities = sorted(df["city"].unique())
selected = st.sidebar.multiselect("Villes", cities, default=cities)
df = df[df["city"].isin(selected)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
latest = df.sort_values("fetched_at").groupby("city").last().reset_index()
col1.metric("Temp. moyenne", f"{latest['temperature'].mean():.1f} °C")
col2.metric("Humidité moy.", f"{latest['humidity'].mean():.0f} %")
col3.metric("Vent max", f"{latest['wind_speed'].max():.1f} m/s")
col4.metric("Villes suivies", len(selected))

st.divider()

# Graphique température dans le temps
fig_temp = px.line(
    df.sort_values("fetched_at"),
    x="fetched_at", y="temperature", color="city",
    title="Évolution des températures",
    labels={"fetched_at": "Heure", "temperature": "°C", "city": "Ville"},
)
st.plotly_chart(fig_temp, use_container_width=True)

col_a, col_b = st.columns(2)

# Humidité par ville
fig_hum = px.bar(
    latest, x="city", y="humidity",
    title="Humidité actuelle (%)", color="humidity",
    color_continuous_scale="Blues",
)
col_a.plotly_chart(fig_hum, use_container_width=True)

# Vent par ville
fig_wind = px.bar(
    latest, x="city", y="wind_speed",
    title="Vitesse du vent (m/s)", color="wind_speed",
    color_continuous_scale="Teal",
)
col_b.plotly_chart(fig_wind, use_container_width=True)

# Table des dernières lectures
st.subheader("Dernières lectures")
st.dataframe(
    latest[["city","temperature","feels_like","humidity","pressure","description","fetched_at"]],
    use_container_width=True,
)