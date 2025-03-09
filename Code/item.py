import json
import os

class Item:
    def __init__(self, icon, name, description, rarity, base_value):
        self.icon = icon
        self.name = name
        self.description = description
        self.rarity = rarity
        self.base_value = base_value

    def inspect_Item(self):
        print(f"{self.icon} {self.name} ({self.rarity})\n"
            f"📜 {self.description}\n"
            f"💰 Value: {self.base_value} 🪙\n")

class Weapon(Item):
    def __init__(self, icon, name, description, rarity, base_value, attack_value):
        super().__init__(icon, name, description, rarity, base_value)
        self.attack_value = attack_value

    def inspect_Item(self):
        super().inspect_Item()
        print(f"⚔️ Attack Bonus: {self.attack_value} AP\n")

class Shield(Item):
    def __init__(self, icon, name, description, rarity, base_value, blocking_value):
        super().__init__(icon, name, description, rarity, base_value)
        self.blocking_value = blocking_value

    def inspect_Item(self):
        super().inspect_Item()
        print(f"🛡 Defense Bonus: {self.blocking_value} DP\n")

class Armor(Item):
    def __init__(self, icon, name, description, rarity, base_value, health_bonus):
        super().__init__(icon, name, description, rarity, base_value)
        self.health_bonus = health_bonus

    def inspect_Item(self):
        super().inspect_Item()
        print(f"❤️ Health Bonus: {self.health_bonus} HP\n")

class Legs(Armor):
    def __init__(self, icon, name, description, rarity, base_value, health_bonus):
        super().__init__(icon, name, description, rarity, base_value)
        self.health_bonus = health_bonus

class ItemLoader:
    @staticmethod
    def load_items_from_json():
        json_path = os.path.join(os.path.dirname(__file__), "../JSON/items.json")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            items_dict = {}
            for name, item_data in data["items"].items():
                item_type = item_data["type"]

                if item_type == "weapon":
                    items_dict[name] = Weapon(
                        item_data["icon"], name, item_data["description"],
                        item_data["rarity"], item_data["base_value"], item_data["attack_value"]
                    )
                elif item_type == "shield":
                    items_dict[name] = Shield(
                        item_data["icon"], name, item_data["description"],
                        item_data["rarity"], item_data["base_value"], item_data["blocking_value"]
                    )
                elif item_type == "armor":
                    items_dict[name] = Armor(
                        item_data["icon"], name, item_data["description"],
                        item_data["rarity"], item_data["base_value"], item_data["health_bonus"]
                    )
                else:
                    items_dict[name] = Item(
                        item_data["icon"], name, item_data["description"],
                        item_data["rarity"], item_data["base_value"]
                    )

            return items_dict

        except FileNotFoundError:
            print("JSON file not found!")
            return {}

        except json.JSONDecodeError:
            print("JSON file is corrupted!")
            return {}

