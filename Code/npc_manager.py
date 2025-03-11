import json
import os
from colors import Colors

def load_npc_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, "npcs.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("npcs.json not found!")
        return {}
    except json.JSONDecodeError:
        print("npcs.json is corrupted!")
        return {}

class NPCManager:
    def __init__(self):
        data = load_npc_data()
        self.npcs = data.get("npcs", {})

    def get_npc_name(self, npc_id):
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

