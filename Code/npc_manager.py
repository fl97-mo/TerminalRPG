import json
import os
import logging
from colors import Colors

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
