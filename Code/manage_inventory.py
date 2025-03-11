from ui_helpers import clear_screen, print_framed

def open_backpack_menu(hero):
    while True:
        clear_screen()
        hero.showInventory()
        print("Backpack Menu:")
        print("1. Use / Equip Item")
        print("2. Discard Item")
        print("c. Close")
        choice = input("Select: ").strip().lower()
        if choice == "1":
            use_item_in_backpack(hero)
        elif choice == "2":
            drop_item_from_backpack(hero)
        elif choice == "c":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

def use_item_in_backpack(hero):
    slot_str = input("Which slot do you want to use (1-20) or c to close: ").strip().lower()
    if slot_str == "c":
        return
    if not slot_str.isdigit():
        print("Invalid Slot Number.")
        input("Press Enter to continue...")
        return
    slot_index = int(slot_str) - 1
    if slot_index < 0 or slot_index >= hero.backpack.capacity:
        print("Slot doesn't exist.")
        input("Press Enter to continue...")
        return
    slot = hero.backpack.slots[slot_index]
    if not slot:
        print("This slot is empty.")
        input("Press Enter to continue...")
        return

    item = slot["item"]
    quantity = slot["quantity"]
    print_framed("Item Info")
    item.inspect_Item()
    print("Quantity: " + str(quantity))
    print("-----------------")
    print("1. Equip")
    print("2. Consume")
    print("c. Cancel")
    action = input("Choice: ").strip().lower()
    if action == "1":
        if hasattr(item, "equip_slots") and item.equip_slots:
            print("Available equip slots:")
            for idx, equip_slot in enumerate(item.equip_slots, start=1):
                print(f"{idx}. {equip_slot}")
            equip_choice = input("Select equip slot (number) or c to cancel: ").strip().lower()
            if equip_choice == "c":
                print("Canceled.")
            elif equip_choice.isdigit():
                equip_idx = int(equip_choice)
                if 1 <= equip_idx <= len(item.equip_slots):
                    chosen_slot = item.equip_slots[equip_idx - 1]
                    success = hero.equip_item(item, chosen_slot)
                    if success:
                        hero.backpack.remove_item(slot_index, 1)
                        print(f"You equipped {item.name} to {chosen_slot}.")
                    else:
                        print("Could not equip item.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        else:
            print("Item is not equipable.")
    elif action == "2":
        hero.backpack.remove_item(slot_index, 1)
        hero.consume_item(item)
        print(f"You used 1x {item.name}.")
    else:
        print("Canceled.")
    input("Press Enter to continue...")

def drop_item_from_backpack(hero):
    slot_str = input("Which slot to discard from (1-20) or c to close: ").strip().lower()
    if slot_str == "c":
        return
    if not slot_str.isdigit():
        print("Invalid Slot number.")
        input("Press Enter to continue...")
        return
    slot_index = int(slot_str) - 1
    if slot_index < 0 or slot_index >= hero.backpack.capacity:
        print("Slot does not exist.")
        input("Press Enter to continue...")
        return
    slot = hero.backpack.slots[slot_index]
    if not slot:
        print("Slot is empty.")
        input("Press Enter to continue...")
        return
    item = slot["item"]
    quantity = slot["quantity"]
    print(f"There are {quantity}x {item.name} in slot {slot_index + 1}.")
    discard_str = input("How many do you want to discard? (enter a number or c to cancel): ").strip().lower()
    if discard_str == "c":
        print("Canceled.")
        input("Press Enter to continue...")
        return
    if not discard_str.isdigit():
        print("Invalid number.")
        input("Press Enter to continue...")
        return
    discard_count = int(discard_str)
    if discard_count < 1 or discard_count > quantity:
        print("Invalid amount.")
        input("Press Enter to continue...")
        return
    hero.backpack.remove_item(slot_index, discard_count)
    print(f"Discarded {discard_count}x {item.name}.")
    input("Press Enter to continue...")

def manage_equipment_slot(hero, slot_name):
    clear_screen()
    item = hero.inventory.get(slot_name)
    if not item:
        print(f"Slot {slot_name} is empty.")
        input("Press Enter to continue...")
        return
    print(f"{slot_name} contains: {item.name}")
    print("1. Inspect")
    print("2. Unequip (move to Backpack)")
    print("c. Cancel")
    action = input("Choice: ").strip().lower()
    if action == "1":
        item.inspect_Item()
    elif action == "2":
        success = hero.unequip_item(slot_name)
        if success:
            print(f"Unequipped {item.name}, moved to backpack.")
    else:
        print("Canceled.")
    input("Press Enter to continue...")

def manage_backpack_slot(hero, slot_index):
    clear_screen()
    slot = hero.backpack.slots[slot_index]
    if not slot:
        print("That backpack slot is empty.")
        input("Press Enter to continue...")
        return
    item = slot["item"]
    qty = slot["quantity"]
    print(f"\nBackpack Slot {slot_index+1}: {item.name} x{qty}")
    print("Possible actions:")
    print("1. Inspect")
    print("2. Equip (move to equipment)")
    print("3. Consume (if consumable)")
    print("4. Discard (some or all)")
    print("c. Cancel")
    action = input("Choice: ").strip().lower()
    if action == "1":
        item.inspect_Item()
    elif action == "2":
        if hasattr(item, "equip_slots") and item.equip_slots:
            print("Available equip slots:")
            for idx, equip_slot in enumerate(item.equip_slots, start=1):
                print(f"{idx}. {equip_slot}")
            equip_choice = input("Select equip slot (number) or c to cancel: ").strip().lower()
            if equip_choice == "c":
                print("Canceled.")
            elif equip_choice.isdigit():
                equip_idx = int(equip_choice)
                if 1 <= equip_idx <= len(item.equip_slots):
                    chosen_slot = item.equip_slots[equip_idx - 1]
                    success = hero.equip_item(item, chosen_slot)
                    if success:
                        hero.backpack.remove_item(slot_index, 1)
                        print(f"You equipped {item.name} to {chosen_slot}.")
                    else:
                        print("Could not equip item.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")
        else:
            print("Item is not equipable.")
    elif action == "3":
        if getattr(item, "is_consumable", False):
            hero.backpack.remove_item(slot_index, 1)
            hero.consume_item(item)
            print(f"You consumed 1x {item.name}.")
        else:
            print("This item is not consumable.")
    elif action == "4":
        discard_str = input(f"How many to discard? (1..{qty}) or c to cancel: ").strip().lower()
        if discard_str == "c":
            print("Canceled.")
            input("Press Enter to continue...")
            return
        if not discard_str.isdigit():
            print("Invalid number.")
            input("Press Enter to continue...")
            return
        discard_count = int(discard_str)
        if discard_count < 1 or discard_count > qty:
            print("Invalid amount.")
            input("Press Enter to continue...")
            return
        hero.backpack.remove_item(slot_index, discard_count)
        print(f"Discarded {discard_count}x {item.name}.")
    else:
        print("Canceled.")
    input("Press Enter to continue...")

def manage_inventory(hero):
    while True:
        clear_screen()
        hero.showInventory()
        print("Inventory Management:")
        print("  E1..E9 => Manage Equipment")
        print("  1..20  => Manage Backpack Slot")
        print("  c      => Back to menu")
        choice = input("Your choice: ").strip().lower()
        if choice == "c":
            break
        if choice.startswith("e"):
            num_str = choice[1:]
            if not num_str.isdigit():
                print("Invalid input. Use E1..E9.")
                input("Press Enter to continue...")
                continue
            slot_idx = int(num_str)
            if slot_idx < 1 or slot_idx > 9:
                print("Equipment slot out of range (1..9).")
                input("Press Enter to continue...")
                continue
            equipment_slots = ["Head", "Armor", "Legs", "Boots", "Left Hand", "Right Hand", "Amulett", "Ring 1", "Ring 2"]
            manage_equipment_slot(hero, equipment_slots[slot_idx - 1])
        else:
            if not choice.isdigit():
                print("Invalid input. Use E1..E9 or 1..20.")
                input("Press Enter to continue...")
                continue
            slot_num = int(choice)
            if slot_num < 1 or slot_num > 20:
                print("Backpack slot out of range (1..20).")
                input("Press Enter to continue...")
                continue
            manage_backpack_slot(hero, slot_num - 1)
