import json
import os
import logging
import random
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
            self.spawn_managers = {}
            for loc_id, loc in self.locations.items():
                if "enemy_spawns" in loc:
                    from npc_manager import SpawnManager
                    self.spawn_managers[loc_id] = SpawnManager(loc)
            self._initialized = True
    def get_start_location(self) -> tuple:
        for loc_id, loc in self.locations.items():
            if loc.get("player_start", False):
                return loc_id, loc
        return None, None

def travel_to_neighbor(hero, game_time):
    lm = LocationManager()
    current_location = lm.locations.get(hero.current_location, {})
    neighbors = current_location.get("neighbors", [])
    if not neighbors:
        print("No available travel destinations.")
        input("Press Enter to continue...")
        return
    print("Available Destinations:")
    for idx, neighbor_id in enumerate(neighbors, start=1):
        neighbor = lm.locations.get(neighbor_id, {})
        print(f"{idx}. {neighbor.get('name', neighbor_id)}")
    choice = input("Choose a destination or press Enter to cancel: ").strip()
    if not choice.isdigit():
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(neighbors):
        print("Invalid selection.")
        input("Press Enter to continue...")
        return

    new_location_id = neighbors[idx]
    neighbor = lm.locations.get(new_location_id, {})
    travel_time = neighbor.get("travel_time", 1)
    print(f"Traveling to {neighbor.get('name', new_location_id)}...")
    for _ in range(travel_time):
        phase, current_time = game_time.wait_turn()
    hero.current_location = new_location_id
    input("Press Enter to continue...")



