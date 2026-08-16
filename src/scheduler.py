from apscheduler.schedulers.blocking import BlockingScheduler
from pipeline import run

scheduler = BlockingScheduler(timezone="Africa/Tunis")

# Exécute le pipeline toutes les heures
scheduler.add_job(run, "interval", hours=1, id="weather_job")

print("Scheduler démarré — pipeline toutes les heures. Ctrl+C pour arrêter.")

try:
    run()  # première exécution immédiate au démarrage
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Scheduler arrêté.")