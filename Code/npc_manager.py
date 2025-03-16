import json
import os
import logging
from colors import Colors
import random

logger = logging.getLogger(__name__)

def load_npc_data() -> dict:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, "npcs.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("npcs.json not found!")
        return {}
    except json.JSONDecodeError:
        logger.error("npcs.json is corrupted!")
        return {}

class NPCManager:
    def __init__(self) -> None:
        data = load_npc_data()
        self.npcs: dict = data.get("npcs", {})
    def get_npc_data(self, npc_id: str) -> dict:
        return self.npcs.get(npc_id, {})
    def get_npc_name(self, npc_id: str) -> str:
        npc_info = self.npcs.get(npc_id)
        if npc_info:
            name = npc_info["name"]
            attitude = npc_info.get("attitude", "Neutral")
            attitude_colors = {
                "Friendly": "Green",
                "Neutral": "Bright White",
                "Hostile": "Bright Red",
                "Feindlich": "Bright Red"
            }
            color = attitude_colors.get(attitude, "Bright White")
            return Colors.color_text(name, color_name=color, style_names="Bold")
        return npc_id

class SpawnManager:
    def __init__(self, location_data):
        self.location_data = location_data
        self.spawn_config = location_data.get("enemy_spawns", {})
        self.current_spawns = {}
        for enemy_id, config in self.spawn_config.items():
            self.current_spawns[enemy_id] = config.get("initial", 0)
        self.last_spawn_round = {enemy_id: 0 for enemy_id in self.spawn_config}
    
    def update_spawns(self, current_round):
        for enemy_id, config in self.spawn_config.items():
            max_count = config.get("max", 0)
            interval = config.get("respawn_interval", 1)
            probability = config.get("respawn_probability", 0.0)
            current_count = self.current_spawns.get(enemy_id, 0)
            
            if current_count < max_count and current_round - self.last_spawn_round[enemy_id] >= interval:
                if random.random() < probability:
                    self.current_spawns[enemy_id] += 1
                    print(f"A new {enemy_id} has spawned! (Total now: {self.current_spawns[enemy_id]})")
                self.last_spawn_round[enemy_id] = current_round

    def enemy_defeated(self, enemy_id):
        if enemy_id in self.current_spawns and self.current_spawns[enemy_id] > 0:
            self.current_spawns[enemy_id] -= 1
            print(f"{enemy_id} defeated. Remaining: {self.current_spawns[enemy_id]}")
