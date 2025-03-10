from character import Hero

class GameMenu:
    @staticmethod
    def open_game_menu(hero):
        while True:
            print("\n----- Game Menu -----")
            print("1. Show Stats")
            print("2. Manage Inventory Items")
            print("3. Close Menu")
            choice = input("Please select an option (1-3): ").strip()
            if choice == "1":
                hero.showStats()
            elif choice == "2":
                GameMenu.manage_inventory(hero)
            elif choice == "3":
                print("Closing menu...")
                break
            else:
                print("Invalid option. Please try again.")

    @staticmethod
    def game_loop(hero):
        print("Type 'm' to open the game menu, or 'q' to quit.")
        while True:
            command = input("Enter command: ").strip().lower()
            if command == "m":
                GameMenu.open_game_menu(hero)
            elif command == "q":
                print("Quitting game. Goodbye!")
                break
            else:
                print("Unknown command. Please type 'm' for menu or 'q' to quit.")

    @staticmethod
    def open_backpack_menu(hero):
        while True:
            hero.showBackpack()
            print("Backpack Menu Options:")
            print("1. Use / Equip Item")
            print("2. Discard Item")
            print("3. Back")

            choice = input("Select: ").strip()
            if choice == "1":
                GameMenu.use_item_in_backpack(hero)
            elif choice == "2":
                GameMenu.drop_item_from_backpack(hero)
            elif choice == "3":
                break
            else:
                print("Invalid option.")

    @staticmethod
    def use_item_in_backpack(hero):
        slot_str = input("Which slot do you want to use (1-20): ").strip()
        if not slot_str.isdigit():
            print("Invalid Slot Number.")
            return
        slot_index = int(slot_str) - 1
        if slot_index < 0 or slot_index >= hero.backpack.capacity:
            print("Slot doesn't exist.")
            return

        slot = hero.backpack.slots[slot_index]
        if not slot:
            print("This slot is empty.")
            return

        item = slot["item"]
        quantity = slot["quantity"]

        print("\n--- Item-Info ---")
        item.inspect_Item()
        print(f"Quantity: {quantity}")
        print("-----------------")

        print("\nWhat do you want to do?")
        print("1. Equip")
        print("2. Consume")
        print("3. Cancel")

        action = input("Choice: ").strip()
        if action == "1":
            # Equip
            if hasattr(item, "attack_value"):
                hero.inventory["Left Hand"] = item
                hero.backpack.remove_item(slot_index, 1)
                print(f"You equipped {item.name}!")
            else:
                print("Item cannot be equipped!")
        elif action == "2":
            hero.backpack.remove_item(slot_index, 1)
            hero.consume_item(item)
            print(f"You used 1x {item.name}.")
        else:
            print("Canceled")


    @staticmethod
    def drop_item_from_backpack(hero):
        slot_str = input("Which Slot do you want to discard? (1-20): ").strip()
        if not slot_str.isdigit():
            print("Invalid Slot number.")
            return
        slot_index = int(slot_str) - 1
        if slot_index < 0 or slot_index >= hero.backpack.capacity:
            print("Slot does not exist.")
            return

        slot = hero.backpack.slots[slot_index]
        if not slot:
            print("Slot is empty.")
            return

        item = slot["item"]
        quantity = slot["quantity"]

        confirm = input(f"Do you really want to remove {quantity}x {item.name} from slot {slot_index+1}? (y/n): ").lower()
        if confirm == "y":
            hero.backpack.remove_item(slot_index, quantity)
            print(f"{item.name} (all {quantity}x) removed.")
        else:
            print("Canceled.")
    @staticmethod
    def manage_backpack_slot(hero, slot_index):
        slot = hero.backpack.slots[slot_index]
        if not slot:
            print("That backpack slot is empty.")
            return

        item = slot["item"]
        qty = slot["quantity"]
        print(f"\nBackpack Slot {slot_index+1}: {item.name} x{qty}")
        print("Possible actions:")
        print("1. Inspect")
        print("2. Equip (move to equipment)")
        print("3. Consume (if consumable)")
        print("4. Discard (some or all from stack)")
        print("5. Cancel")
        action = input("Choice: ").strip()

        if action == "1":
            item.inspect_Item()

        elif action == "2":
            if not item.equip_slots:
                print("This item cannot be equipped (no equip_slots defined).")
                return

            print("Where do you want to equip it?")
            for i, eslot in enumerate(item.equip_slots, start=1):
                print(f"{i}. {eslot}")

            choice_slot_str = input("Select a slot number: ").strip()
            if not choice_slot_str.isdigit():
                print("Invalid input.")
                return
            choice_slot_num = int(choice_slot_str)
            if choice_slot_num < 1 or choice_slot_num > len(item.equip_slots):
                print("Slot choice out of range.")
                return
            target_slot = item.equip_slots[choice_slot_num - 1]

            # 1) Remove 1 from Backpack
            removed_ok = hero.backpack.remove_item(slot_index, 1)
            if not removed_ok:
                print("Could not remove item from backpack.")
                return

            # 2)  equip in hero
            success = hero.equip_item(item, target_slot)
            if not success:
                hero.backpack.add_item(item, 1)
            else:
                print(f"Equipped {item.name} to {target_slot}.")

        elif action == "3":  # Consume
            if getattr(item, "is_consumable", False):
                hero.backpack.remove_item(slot_index, 1)
                hero.consume_item(item)
                print(f"You consumed 1x {item.name}.")
            else:
                print("This item is not consumable.")


        elif action == "4":  # Discard
            amount_str = input(f"How many do you want to discard? (1..{qty}): ").strip()
            if not amount_str.isdigit():
                print("Invalid number.")
                return
            amount = int(amount_str)
            if amount < 1 or amount > qty:
                print("Invalid amount.")
                return
            hero.backpack.remove_item(slot_index, amount)
            print(f"Discarded {amount}x {item.name}.")

        else:
            print("Canceled.")
    @staticmethod
    def manage_equipment_slot(hero, slot_name):
        item = hero.inventory.get(slot_name)
        if not item:
            print(f"Slot {slot_name} is empty.")

            return

        print(f"{slot_name} contains: {item.name}")
        print("1. Inspect")
        print("2. Unequip (move to Backpack)")
        print("3. Cancel")
        action = input("Choice: ").strip()

        if action == "1":
            item.inspect_Item()
        elif action == "2":
            success = hero.unequip_item(slot_name)
            if success:
                print(f"Unequipped {item.name}, moved to backpack.")
        else:
            print("Canceled.")

    @staticmethod
    def manage_inventory(hero):
        while True:
            hero.showInventory()
            print("Select a slot to manage:")
            print("  E1..E9 => Equipment")
            print("  1..20  => Backpack slot number")
            print("  X => Back to menu")

            choice = input("Your choice: ").strip().lower()
            if choice == "x":
                break

            # Check if equipment:
            if choice.startswith("e"):
                num_str = choice[1:]
                if not num_str.isdigit():
                    print("Invalid input. Use E1..E9.")
                    continue
                slot_idx = int(num_str)
                if slot_idx < 1 or slot_idx > 9:
                    print("Equipment slot out of range (1..9).")
                    continue
                eq_slots = [
                    "Head", "Armor", "Legs", "Boots",
                    "Left Hand", "Right Hand",
                    "Amulett", "Ring 1", "Ring 2"
                ]
                slot_name = eq_slots[slot_idx - 1]
                GameMenu.manage_equipment_slot(hero, slot_name)

            else:
                if not choice.isdigit():
                    print("Invalid input. Use E1..E9 or 1..20.")
                    continue
                slot_num = int(choice)
                if slot_num < 1 or slot_num > 20:
                    print("Backpack slot out of range (1..20).")
                    continue

                GameMenu.manage_backpack_slot(hero, slot_num - 1)