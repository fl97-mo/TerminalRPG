from character import *
from item import *

def main():

    hero_inventory = {0:"Wooden Sword"}
    hero_equipped = {
    "Helmet": None,
    "Amulet": None,
    "Armor": None,
    "Gloves": None,
    "Weapon": None,
    "Ring": None,
    "Shield": None,
    "Pants": None,
    "Boots": None
    }

    all_items = Item.load_items_from_json()


    hero_name = input(f"Enter your heroes name:\n")
    hero = Hero(hero_name, 100, 100, 10, 0, None, hero_inventory)

    hero.showStats()
    hero.showInventory()


    for item in all_items.values():
        item.inspect_Item()
        print("-" * 40)

if __name__ == "__main__":
    main ()