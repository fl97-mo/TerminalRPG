import json
import os

def load_json(filename):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(filename + " not found!")
        return {}
    except json.JSONDecodeError:
        print(filename + " is corrupted!")
        return {}

class LocationManager:
    def __init__(self):
        data = load_json("locations.json")
        self.locations = data.get("locations", {})
        self.buildings = data.get("buildings", {})
        self.containers = data.get("containers", {})

    def get_start_location(self):
        for loc_id, loc in self.locations.items():
            if loc.get("player_start", False):
                return loc_id, loc
        return None, None
