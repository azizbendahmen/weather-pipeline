# weather-pipeline

Pipeline ETL qui collecte des données météo toutes les heures et les stocke dans PostgreSQL.

**Stack :** Python · Pandas · PostgreSQL · Streamlit · Docker · APScheduler

---

## Ce que ça fait

1. Appelle l'API OpenWeatherMap pour plusieurs villes
2. Nettoie et valide les données (températures aberrantes, champs manquants)
3. Insère dans PostgreSQL
4. Affiche un dashboard Streamlit avec l'historique


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

## Tests

```bash
pytest tests/ -v
```
