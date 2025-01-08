from flask import Flask, current_app
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from sync.server.config import read_config


def sync_task(synchro):
    """Fonction de synchronisation principale."""
    print(f"Synchronization started at {datetime.now()} - with params: {synchro}")

def start_scheduler(app):
    print("Starting scheduler...")
    config = read_config()
    synchros = config.get('synchros')
    scheduler = BackgroundScheduler()

    for synchro in synchros:
        if synchro.get('enabled'):
            scheduler.add_job(sync_task, 'interval', seconds=synchro.get('interval'), args=[synchro])
    scheduler.start()
