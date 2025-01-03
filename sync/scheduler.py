from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def sync_task():
    """Fonction de synchronisation principale."""
    print(f"Synchronization started at {datetime.now()}")

def start_scheduler():
    """Démarrer le scheduler."""
    print("Starting scheduler...")
    scheduler = BackgroundScheduler()

    scheduler.add_job(sync_task, 'interval', seconds=5)
    scheduler.start()
