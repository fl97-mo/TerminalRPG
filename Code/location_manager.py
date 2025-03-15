import json
import os
import logging

logger = logging.getLogger(__name__)

def load_json(filename: str) -> dict:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"{filename} not found!")
        return {}
    except json.JSONDecodeError:
        logger.error(f"{filename} is corrupted!")
        return {}

class LocationManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            data = load_json("locations.json")
            self.locations = data.get("locations", {})
            self.buildings = data.get("buildings", {})
            self.containers = data.get("containers", {})
            self._initialized = True
    def get_start_location(self) -> tuple:
        for loc_id, loc in self.locations.items():
            if loc.get("player_start", False):
                return loc_id, loc
        return None, None