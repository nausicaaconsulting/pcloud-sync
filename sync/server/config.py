import json
import os

from sync import settings

def read_config():
    """Lire le fichier config.json."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(project_dir, settings.CONFIG_FILE)):
        print(f"Config file {settings.CONFIG_FILE} not found. Returning empty config.")
        return {}
    with open(settings.CONFIG_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error reading {settings.CONFIG_FILE}: {e}")
            return {}

def write_config(data):
    """Écrire dans le fichier config.json."""
    with open(settings.CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)
