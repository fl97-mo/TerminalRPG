import json
import os
import random
from item import ItemLoader

class Shop:
    def __init__(self, shop_id, data):
        self.shop_id = shop_id
        self.theme = data.get("theme", "default")
        self.refresh_interval = data.get("refresh_interval", 24)
        self.gold = data.get("gold", 100)

        self.items_data = data.get("items", [])
        self.inventory = []

        self.generate_inventory()

    def generate_inventory(self):
        self.inventory = []
        all_items = ItemLoader.load_items_from_json()

        for entry in self.items_data:
            item_name = entry["name"]
            quantity = entry["quantity"]
            chance = entry.get("chance", 1.0)

            if random.random() <= chance:
                if item_name in all_items:
                    item_obj = all_items[item_name]
                    self.inventory.append({
                        "item": item_obj,
                        "quantity": quantity
                    })
                else:
                    print(f"[ShopManager] Item '{item_name}' not found in items.json")
    
    def find_item_in_shop(self, item_name):
        for slot in self.inventory:
            if slot["item"].name == item_name:
                return slot
        return None

    def buy_item(self, item_slot, hero, quantity):
        total_cost = item_slot["item"].base_value * quantity
        if hero.gold < total_cost:
            print("You do not have enough gold.")
            return False

        if item_slot["quantity"] < quantity:
            print("The shop doesn't have enough of that item.")
            return False
        
        hero.gold -= total_cost
        item_slot["quantity"] -= quantity
        hero.addToBackpack(item_slot["item"], quantity)
        
        print(f"You bought {quantity}x {item_slot['item'].name} for {int(total_cost)} gold.")
        return True

    def sell_item_to_shop(self, hero, slot_index, quantity):
        if slot_index < 0 or slot_index >= hero.backpack.capacity:
            print("Invalid backpack slot.")
            return False
        slot = hero.backpack.slots[slot_index]
        if not slot:
            print("No item in that slot.")
            return False
        
        if slot["quantity"] < quantity:
            print("You don't have that many items in this slot.")
            return False

        item_obj = slot["item"]
        total_value = item_obj.base_value * 0.5 * quantity

        if self.gold < total_value:
            print("Shop does not have enough gold to buy these items.")
            return False

        self.gold -= total_value
        hero.gold += total_value

        hero.removeFromBackpack(slot_index, quantity)

        existing_slot = self.find_item_in_shop(item_obj.name)
        if existing_slot is None:
            self.inventory.append({
                "item": item_obj,
                "quantity": quantity
            })
        else:
            existing_slot["quantity"] += quantity

        print(f"You sold {quantity}x {item_obj.name} for {int(total_value)} gold.")
        return True

class ShopManager:
    def __init__(self):
        self.shops_data = {}
        self.shops_instances = {}
        self.load_shops_json()

    def load_shops_json(self):
        base_path = os.path.dirname(__file__)
        filepath = os.path.join(base_path, "../JSON/shops.json")
        if not os.path.exists(filepath):
            print(f"[ShopManager] shops.json not found at {filepath}")
            return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.shops_data = data.get("shops", {})

    def get_shop(self, shop_id):
        if shop_id in self.shops_instances:
            return self.shops_instances[shop_id]
        if shop_id in self.shops_data:
            shop_info = self.shops_data[shop_id]
            shop_obj = Shop(shop_id, shop_info)
            self.shops_instances[shop_id] = shop_obj
            return shop_obj
        else:
            print(f"[ShopManager] Unknown shop_id '{shop_id}'")
            return None



def open_shop_menu(hero, shop):
    while True:
        print("\n--- Shop Menu ---")
        print(f"Shop Gold: {int(shop.gold)}   |   Your Gold: {int(hero.gold)}")
        print("Items in Shop:")
        idx = 1
        for slot in shop.inventory:
            item_obj = slot["item"]
            qty = slot["quantity"]
            print(f"{idx}. {item_obj.name} (Qty: {qty}, Price: {int(item_obj.base_value)})")
            idx += 1

        print("\nYour Options:")
        print("b. Buy Item")
        print("v. Sell Item")
        print("x. Exit Shop")

        choice = input("Choice: ").strip().lower()
        if choice == "x":
            break
        elif choice == "b":
            buy_index_str = input("Which shop item do you want to buy? (or Enter to cancel): ").strip()
            if not buy_index_str.isdigit():
                continue
            buy_index = int(buy_index_str) - 1
            if buy_index < 0 or buy_index >= len(shop.inventory):
                continue
            quantity_str = input("How many to buy?: ").strip()
            if not quantity_str.isdigit():
                continue
            quantity = int(quantity_str)
            shop.buy_item(shop.inventory[buy_index], hero, quantity)

        elif choice == "v":
            print("Which backpack slot do you want to sell from? (1..20)")
            slot_str = input("Slot: ").strip()
            if not slot_str.isdigit():
                continue
            slot_index = int(slot_str) - 1
            quantity_str = input("How many do you want to sell?: ").strip()
            if not quantity_str.isdigit():
                continue
            quantity = int(quantity_str)
            shop.sell_item_to_shop(hero, slot_index, quantity)

