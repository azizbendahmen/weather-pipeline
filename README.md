# weather-pipeline

Pipeline ETL qui collecte des données météo toutes les heures et les stocke dans PostgreSQL.

**Stack :** Python · Pandas · PostgreSQL · Streamlit · Docker · APScheduler

---

## Ce que ça fait

1. Appelle l'API OpenWeatherMap pour plusieurs villes
2. Nettoie et valide les données (températures aberrantes, champs manquants)
3. Insère dans PostgreSQL
4. Affiche un dashboard Streamlit avec l'historique

## Lancer le projet

**Prérequis :** Python 3.11+, Docker

```bash
git clone https://github.com/azizbendahmen/weather-pipeline.git
cd weather-pipeline

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env      # remplir avec ta clé API
docker compose up -d      # lance PostgreSQL
```

**Exécuter le pipeline une fois :**
```bash
cd src && python pipeline.py
```

**Lancer le scheduler (toutes les heures) :**
```bash
cd src && python scheduler.py
```

**Dashboard :**
```bash
streamlit run dashboard/app.py
```
## Structure

```
weather-pipeline/
├── src/
│   ├── extract.py       # appel API OpenWeatherMap
│   ├── transform.py     # nettoyage + validation
│   ├── load.py          # insertion PostgreSQL
│   ├── pipeline.py      # orchestration ETL
│   └── scheduler.py     # exécution horaire
├── dashboard/
│   └── app.py           # interface Streamlit
├── tests/
│   └── test_transform.py
├── docker-compose.yml
└── .env.example
```
