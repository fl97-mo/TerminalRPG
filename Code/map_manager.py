import json
import os
from asciimap import AsciiMap

def load_maps_json():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, "maps.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("maps.json not found!")
        return {}
    except json.JSONDecodeError:
        print("maps.json is corrupted!")
        return {}

class MapManager:
    def __init__(self):
        data = load_maps_json()
        self.maps = data.get("maps", {})

    def create_ascii_map(self, map_id, title_line1="", title_line2=""):
        map_info = self.maps.get(map_id)
        if not map_info:
            print(f"[MapManager] Map ID '{map_id}' not found.")
            return None
        
        theme = map_info.get("theme", "temperate forest")
        map_data = map_info.get("data", [])
        
        ascii_map = AsciiMap(map_data, theme=theme)
        
        ascii_map.print_banner_above_map(title_line1, title_line2)
        
        return ascii_map
