import textwrap
from ui_helpers import clear_screen, print_framed, print_three_column_screen
from location_manager import LocationManager
from item import ItemLoader
from map_manager import MapManager



def open_container(hero, container_info: dict, items_data: dict, container_id: str) -> None:
    clear_screen()
    print_framed("Opening " + container_info.get("name", "Unknown Container"))

    if not container_info.get("contains"):
        print("It is empty.")
        input("Press Enter to continue...")
        return

    while True:
        print("\nItems in " + container_info.get("name", "Unknown Container") + ":")
        for idx, itm in enumerate(container_info["contains"], start=1):
            print(f"{idx}. {itm}")
        print("a. Take all")
        print("c. Cancel")
        choice = input("Choose an option: ").strip().lower()

        if choice == "a":
            taken_items = []
            for itm in container_info["contains"]:
                if itm in items_data:
                    hero.addToBackpack(items_data[itm])
                    taken_items.append(itm)
                    print("Took " + itm + ".")
            count = len(taken_items)
            container_info["contains"].clear()
            hero.quest_log.check_triggers("collect", hero, container_id=container_id, count=count)
            input("Press Enter to continue...")
            return

        elif choice == "c":
            return

        else:
            if not choice.isdigit():
                print("Invalid choice.")
                input("Press Enter to continue...")
                continue
            pick_index = int(choice) - 1
            if pick_index < 0 or pick_index >= len(container_info["contains"]):
                print("Invalid choice.")
                input("Press Enter to continue...")
                continue
            item_to_take = container_info["contains"][pick_index]
            if item_to_take not in items_data:
                print("Cannot find " + item_to_take + " in items database.")
                input("Press Enter to continue...")
                continue
            hero.addToBackpack(items_data[item_to_take])
            print("Took " + item_to_take + ".")
            container_info["contains"].pop(pick_index)
            hero.quest_log.check_triggers("collect", hero, container_id=container_id, count=1)
            input("Press Enter to continue...")
            clear_screen()
            print_framed("Opening " + container_info.get("name", "Unknown Container"))

def enter_building(hero) -> None:
    from ui_helpers import clear_screen, print_framed, print_three_column_screen
    from location_manager import LocationManager
    from item import ItemLoader
    from map_manager import MapManager
    lm = LocationManager()
    map_manager = MapManager()
    items_data = ItemLoader.load_items_from_json()
    buildings_data = lm.buildings
    containers_data = lm.containers
    if hero.current_location not in lm.locations:
        print("You are at an unknown location.")
        input("Press Enter to return...")
        return

    current_location = lm.locations[hero.current_location]
    building_ids = current_location.get("buildings", [])
    if not building_ids:
        print("There are no buildings here.")
        input("Press Enter to return...")
        return

    location_buildings = []
    for b_id in building_ids:
        if b_id in buildings_data:
            location_buildings.append((b_id, buildings_data[b_id]))
    if not location_buildings:
        print("There are no buildings here.")
        input("Press Enter to return...")
        return

    print_framed("Buildings")
    for idx, (b_id, b_info) in enumerate(location_buildings, start=1):
        print(f"{idx}. {b_info.get('name', b_id)}")
    print("Press Enter to return.")
    choice = input("Enter building number: ").strip().lower()
    if choice == "":
        confirm = input("Press Enter to confirm return or type 'c' to cancel: ").strip().lower()
        if confirm == "":
            return
    if not choice.isdigit():
        print("Invalid choice.")
        input("Press Enter to return...")
        return
    choice_num = int(choice)
    if choice_num < 1 or choice_num > len(location_buildings):
        print("Invalid choice.")
        input("Press Enter to return...")
        return

    selected_building_id, selected_building = location_buildings[choice_num - 1]
    print("You entered " + selected_building.get("name", selected_building_id) + ".")
    input("Press Enter to continue...")
    hero.current_building = selected_building_id

    while True:
        clear_screen()
        left_lines = [
            "Containers in:",
            selected_building.get("name", "Unknown Building"),
            ""
        ]
        container_ids = selected_building.get("containers", [])
        if container_ids:
            left_lines.append("You see:")
            for idx, c_id in enumerate(container_ids, start=1):
                c_info = containers_data.get(c_id)
                if c_info:
                    left_lines.append(f"{idx}. {c_info.get('name', c_id)}")
        else:
            left_lines.append("(No containers here)")
        left_lines.append("")
        left_lines.append("Press Enter to return")
        middle_lines = []
        b_name = selected_building.get("name", "Unknown Building")
        b_faction = selected_building.get("faction", "Unknown")
        b_type = selected_building.get("type", "Unknown")
        b_desc = selected_building.get("description", "No description provided.")
        middle_lines.append(b_name)
        middle_lines.append(f"Faction: {b_faction}")
        middle_lines.append(f"Type: {b_type}")
        import textwrap
        desc_wrapped = textwrap.wrap(f"Description: {b_desc}", width=40)
        middle_lines.extend(desc_wrapped)
        right_lines = []
        building_map_id = selected_building.get("map_id")
        banner_line1 = ""
        banner_line2 = ""
        wrapped_banner = textwrap.wrap(b_name, width=30)
        if wrapped_banner:
            banner_line1 = wrapped_banner[0]
            if len(wrapped_banner) > 1:
                banner_line2 = wrapped_banner[1]
        if building_map_id:
            ascii_map_obj = map_manager.create_ascii_map(building_map_id, banner_line1, banner_line2)
            if ascii_map_obj:
                rendered_map = ascii_map_obj.draw_map()
                right_lines = rendered_map.split("\n")
            else:
                right_lines = ["[Error loading building map]"]
        else:
            right_lines = ["No map available"]

        print_three_column_screen(
            left_lines,
            middle_lines,
            right_lines,
            left_title="Building Menu",
            middle_title="Building Info",
            right_title="Map"
        )
        c_choice = input("Choose a container (or press Enter to exit building): ").strip().lower()
        if c_choice == "":
            hero.current_building = None
            print("You exit the building and return to the open area.")
            input("Press Enter to continue...")
            break
        if not c_choice.isdigit():
            print("Invalid choice.")
            input("Press Enter to return...")
            continue
        c_num = int(c_choice)
        if c_num < 1 or c_num > len(container_ids):
            print("Invalid choice.")
            input("Press Enter to return...")
            continue
        container_id = container_ids[c_num - 1]
        if container_id not in containers_data:
            print("No information about this container.")
            input("Press Enter to return...")
            continue
        from building_menu import open_container
        open_container(hero, containers_data[container_id], items_data, container_id)
