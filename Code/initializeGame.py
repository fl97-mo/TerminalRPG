from character import Hero, NPC
from item import ItemLoader
from dialog import Dialog
from validations import get_validated_name
from location_manager import LocationManager
import logging

logger = logging.getLogger(__name__)

def create_new_game() -> Hero:
    locations = LocationManager()
    start_location_id, start_location = locations.get_start_location()
    
    if not start_location:
        logger.error("Error: No starting location found!")
        return None
    
    all_items = ItemLoader.load_items_from_json()
    hero_inventory = {
        "Head": None,
        "Armor": all_items.get("Tattered Rags"),
        "Legs": all_items.get("Torn Leather Trousers"),
        "Boots": all_items.get("Worn-out sandals"),
        "Left Hand": all_items.get("Wooden Sword"),
        "Right Hand": all_items.get("Wooden Shield"),
        "Amulett": None,
        "Ring 1": None,
        "Ring 2": None
    }

    dialogues = Dialog.load_dialogues()
    old_man_dialogues = dialogues.get("Old Man", {})
    old_man = NPC("Old Man", 100, 100, 10, 1, None, old_man_dialogues, npc_id="npc_old_man")

    old_man.talk(1)
    hero_name = get_validated_name("Enter your hero's name: ")
    background = old_man.talk(2, hero_name=hero_name)

    hero = Hero(hero_name, 100, 100, 10, 0, background, hero_inventory)
    hero.current_location = start_location_id
    hero.addToBackpack(all_items["Healing Potion"], quantity=5)
    hero.addToBackpack(all_items["Wooden Sword"], quantity=1)
    return hero
