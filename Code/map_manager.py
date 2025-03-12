import json
import os
import logging
from asciimap import AsciiMap

logger = logging.getLogger(__name__)

def load_maps_json() -> dict:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../JSON"))
    filepath = os.path.join(base_path, "maps.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("maps.json not found!")
        return {}
    except json.JSONDecodeError:
        logger.error("maps.json is corrupted!")
        return {}

class MapManager:
    def __init__(self) -> None:
        data = load_maps_json()
        self.maps: dict = data.get("maps", {})

    def create_ascii_map(self, map_id: str, title_line1: str = "", title_line2: str = "") -> AsciiMap:
        map_info = self.maps.get(map_id)
        if not map_info:
            logger.error(f"[MapManager] Map ID '{map_id}' not found.")
            return None
        
        theme = map_info.get("theme", "temperate forest")
        map_data = map_info.get("data", [])
        
        ascii_map = AsciiMap(map_data, theme=theme)
        ascii_map.print_banner_above_map(title_line1, title_line2)
        
        return ascii_map
