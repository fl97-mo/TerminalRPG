from character import Hero, NPC
from item import ItemLoader
from dialog import Dialog

def create_new_game():
    all_items = ItemLoader.load_items_from_json()

    hero_inventory = {
        "Weapon": all_items.get("Wooden Sword"),
        "Shield": all_items.get("Wooden Shield"),
        "Armor":  all_items.get("Tattered Rags"),
        "Legs":   all_items.get("Torn Leather Trousers"),
        "Boots":  all_items.get("Worn-out sandals")
    }
    # load dialogue
    dialogues = Dialog.load_dialogues()
    old_man_dialogues = dialogues.get("OldMan", {})

    # create - old man
    old_man = NPC("OldMan", health=100, stamina=100, attack=10, level=1, guild=None, dialogues=old_man_dialogues)

    # intro convo
    old_man.talk(1)
    hero_name = input("Enter your hero's name: ")

    background = old_man.talk(2, hero_name=hero_name)

    # create hero
    hero = Hero(hero_name, health=100, stamina=100, attack=10, level=0, guild=background, inventory=hero_inventory)
    return hero
