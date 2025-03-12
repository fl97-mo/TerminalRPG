import json
import os
from typing import Dict
from colors import Colors

RARITY_COLORS: Dict[str, str] = {
    "common": "\033[90m",
    "uncommon": "\033[92m",
    "rare": "\033[96m",
    "epic": "\033[95m",
    "legendary": "\033[93m"
}
RESET_COLOR = "\033[0m"

def get_rarity_color(rarity_str: str) -> str:
    return RARITY_COLORS.get(rarity_str.lower(), "")

class Item:
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 stackable: bool = True, stack_limit: int = 64, equip_slots=None):
        self.icon = icon
        self.name = name
        self.description = description
        self.rarity = rarity
        self.base_value = base_value
        self.stackable = stackable
        self.stack_limit = stack_limit
        self.equip_slots = equip_slots if equip_slots else []

    def inspect_Item(self) -> None:
        color_code = get_rarity_color(self.rarity)
        print(f"{color_code}{self.icon} {self.name} ({self.rarity}){RESET_COLOR}\n"
              f"📜 {self.description}\n"
              f"💰 Value: {self.base_value} 🪙\n")

class Consumable(Item):
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 stackable: bool = True, stack_limit: int = 64, equip_slots=None, heal_value: int = 0):
        super().__init__(icon, name, description, rarity, base_value, stackable, stack_limit, equip_slots)
        self.is_consumable = True
        self.heal_value = heal_value

    def inspect_Item(self) -> None:
        super().inspect_Item()
        print("🍴 This item can be consumed.")
        if self.heal_value > 0:
            print(f"It will heal {self.heal_value} HP.\n")
        else:
            print()

class Weapon(Item):
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 attack_value: int, stackable: bool = True, stack_limit: int = 64, equip_slots=None):
        super().__init__(icon, name, description, rarity, base_value, stackable, stack_limit, equip_slots)
        self.attack_value = attack_value

    def inspect_Item(self) -> None:
        super().inspect_Item()
        print(f"⚔️ Attack Bonus: {self.attack_value} AP\n")

class Shield(Item):
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 blocking_value: int, stackable: bool = True, stack_limit: int = 64, equip_slots=None):
        super().__init__(icon, name, description, rarity, base_value, stackable, stack_limit, equip_slots)
        self.blocking_value = blocking_value

    def inspect_Item(self) -> None:
        super().inspect_Item()
        print(f"🛡 Defense Bonus: {self.blocking_value} DP\n")

class Armor(Item):
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 health_bonus: int, stackable: bool = True, stack_limit: int = 64, equip_slots=None):
        super().__init__(icon, name, description, rarity, base_value, stackable, stack_limit, equip_slots)
        self.health_bonus = health_bonus

    def inspect_Item(self) -> None:
        super().inspect_Item()
        print(f"❤️ Health Bonus: {self.health_bonus} HP\n")

class Legs(Armor):
    def __init__(self, icon: str, name: str, description: str, rarity: str, base_value: float,
                 health_bonus: int, stackable: bool = True, stack_limit: int = 64, equip_slots=None):
        super().__init__(icon, name, description, rarity, base_value, health_bonus, stackable, stack_limit, equip_slots)

class ItemLoader:
    @staticmethod
    def load_items_from_json() -> Dict[str, Item]:
        json_path = os.path.join(os.path.dirname(__file__), "../JSON/items.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            items_dict: Dict[str, Item] = {}
            for name, item_data in data["items"].items():
                item_type = item_data["type"].lower()
                stackable = item_data.get("stackable", True)
                stack_limit = item_data.get("stack_limit", 64)
                equip_slots = item_data.get("equip_slots", [])
                if item_type == "weapon":
                    items_dict[name] = Weapon(
                        icon=item_data["icon"],
                        name=name,
                        description=item_data["description"],
                        rarity=item_data["rarity"],
                        base_value=item_data["base_value"],
                        attack_value=item_data["attack_value"],
                        stackable=stackable,
                        stack_limit=stack_limit,
                        equip_slots=equip_slots
                    )
                elif item_type == "shield":
                    items_dict[name] = Shield(
                        icon=item_data["icon"],
                        name=name,
                        description=item_data["description"],
                        rarity=item_data["rarity"],
                        base_value=item_data["base_value"],
                        blocking_value=item_data["blocking_value"],
                        stackable=stackable,
                        stack_limit=stack_limit,
                        equip_slots=equip_slots
                    )
                elif item_type in ["armor", "legs", "boots"]:
                    items_dict[name] = Armor(
                        icon=item_data["icon"],
                        name=name,
                        description=item_data["description"],
                        rarity=item_data["rarity"],
                        base_value=item_data["base_value"],
                        health_bonus=item_data["health_bonus"],
                        stackable=stackable,
                        stack_limit=stack_limit,
                        equip_slots=equip_slots
                    )
                elif item_type == "consumable":
                    heal_val = item_data.get("heal_value", 0)
                    items_dict[name] = Consumable(
                        icon=item_data["icon"],
                        name=name,
                        description=item_data["description"],
                        rarity=item_data["rarity"],
                        base_value=item_data["base_value"],
                        stackable=stackable,
                        stack_limit=stack_limit,
                        equip_slots=equip_slots,
                        heal_value=heal_val
                    )
                else:
                    items_dict[name] = Item(
                        icon=item_data["icon"],
                        name=name,
                        description=item_data["description"],
                        rarity=item_data["rarity"],
                        base_value=item_data["base_value"],
                        stackable=stackable,
                        stack_limit=stack_limit,
                        equip_slots=equip_slots
                    )
            return items_dict
        except FileNotFoundError:
            print("JSON file not found!")
            return {}
        except json.JSONDecodeError:
            print("JSON file is corrupted!")
            return {}
