import json
import os

class Item():
    def __init__(self, icon, name, description, rarity, base_value):
        self.icon = icon
        self.name = name 
        self.description = description
        self.rarity = rarity
        self.base_value = base_value

    def inspect_Item(self):
        print(f"Name:   {self.name}\n"
            f"Icon:   {self.icon}\n"
            f"Story:  {self.description}\n"
            f"Rarity: {self.rarity}\n"
            f"Value:  {self.base_value} 🪙\n")


class Helmet(Item):
    pass
class Amulet(Item):
    pass
class Armor(Item):
    pass
class Gloves(Item):
    pass
class Weapon(Item):
    pass
class Ring(Item):
    pass
class Shield(Item):
    pass
class Pants(Item):
    pass
class Boots(Item):
    pass
