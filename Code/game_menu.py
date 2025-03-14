import textwrap
from ui_helpers import clear_screen, print_framed, print_three_column_screen
from manage_inventory import open_backpack_menu, manage_inventory
from building_menu import enter_building
from dialog_menu import talk_to_npc
from location_manager import LocationManager
from npc_manager import NPCManager
from map_manager import MapManager

def look_around(hero) -> None:
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()
    loc = lm.locations.get(hero.current_location, {})
    if loc:
        print_framed(f"{loc.get('name', hero.current_location)} ({loc.get('type', 'Unknown')})")
        if loc.get("npcs"):
            print("People here:")
            for npc in loc["npcs"]:
                print(" - " + npc_m.get_npc_name(npc))
        else:
            print("Nobody is here.")
        if loc.get("buildings"):
            print("Buildings:")
            for building in loc["buildings"]:
                if building in lm.buildings:
                    print(" - " + lm.buildings[building]["name"])
        else:
            print("No buildings found.")
    else:
        print("Unknown location.")
    input("Press Enter to continue...")

def open_game_menu(hero) -> None:
    lm = LocationManager()
    map_manager = MapManager()

        # Add helper functions INSIDE open_game_menu but BEFORE the main loop
    def show_quest_log(hero):
        while True:
            clear_screen()
            print_framed("Quest Log")
            print("1. Active Quests")
            print("2. Completed Quests")
            print("c. Cancel")
            log_choice = input("Choose an option: ").strip().lower()
            if log_choice == "1":
                display_active_quests(hero)
            elif log_choice == "2":
                display_completed_quests(hero)
            elif log_choice == "c":
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def display_active_quests(hero):
        clear_screen()
        print_framed("Active Quests")
        if not hero.quest_log.active_quests:
            print("No active quests.")
        else:
            for idx, quest in enumerate(hero.quest_log.active_quests, start=1):
                print(f"{idx}. {quest.name}")
                print(f"   {quest.description}")
                print("   Objectives:")
                for obj in quest.objectives:
                    status = f"{obj.current}/{obj.required}" if not obj.completed else "Completed"
                    print(f"   - {obj.description} [{status}]")
                print()
        input("Press Enter to continue...")

    def display_completed_quests(hero):
        clear_screen()
        print_framed("Completed Quests")
        if not hero.quest_log.completed_quests:
            print("No completed quests.")
        else:
            for idx, quest in enumerate(hero.quest_log.completed_quests, start=1):
                print(f"{idx}. {quest.name}")
                print(f"   {quest.description}")
        input("Press Enter to continue...")


    while True:
        clear_screen()
        if hero.current_building:
            left_lines = [
                "1. Show Stats",
                "2. Look around",
                "3. Manage Inventory Items",
                "4. Enter Building",
                "5. Talk to NPC",
                "6. Quest Log",
                "c. Close Menu"
            ]
            middle_title = "Building"
            b_info = lm.buildings.get(hero.current_building, {})
            b_name = b_info.get("name", "Unknown Building")
            b_desc = b_info.get("description", "No description provided.")
            b_faction = b_info.get("faction", "Unknown")
            b_type = b_info.get("type", "Unknown")
            wrapped_desc = textwrap.wrap(f"Description: {b_desc}", width=40)
            middle_lines = [
                f"Faction: {b_faction}",
                f"Type: {b_type}"
            ]
            middle_lines.extend(wrapped_desc)
            map_id = b_info.get("map_id")
            banner_line1 = ""
            banner_line2 = ""
            if b_name:
                wrapped_banner = textwrap.wrap(b_name, width=30)
                if wrapped_banner:
                    banner_line1 = wrapped_banner[0]
                    if len(wrapped_banner) > 1:
                        banner_line2 = wrapped_banner[1]
            if map_id:
                ascii_map_obj = map_manager.create_ascii_map(map_id, banner_line1, banner_line2)
                if ascii_map_obj:
                    rendered = ascii_map_obj.draw_map()
                    map_lines = rendered.split("\n")
                else:
                    map_lines = ["[Error loading Map]"]
            else:
                map_lines = ["No map available"]
        else:
            left_lines = [
                "1. Show Stats",
                "2. Look around",
                "3. Manage Inventory Items",
                "4. Enter Building",
                "5. Talk to NPC",
                "6. Quest Log",
                "c. Close Menu"
            ]
            middle_title = "Location"
            loc_info = lm.locations.get(hero.current_location, {})
            loc_name = loc_info.get("name", "Unknown Location")
            loc_desc = loc_info.get("description", "No description provided.")
            loc_faction = loc_info.get("faction", "Unknown")
            loc_type = loc_info.get("type", "Unknown")
            wrapped_desc = textwrap.wrap(f"Description: {loc_desc}", width=40)
            middle_lines = [
                loc_name,
                f"Faction: {loc_faction}",
                f"Type: {loc_type}"
            ]
            middle_lines.extend(wrapped_desc)
            map_id = loc_info.get("map_id")
            banner_line1 = ""
            banner_line2 = ""
            if loc_name:
                wrapped_banner = textwrap.wrap(loc_name, width=30)
                if wrapped_banner:
                    banner_line1 = wrapped_banner[0]
                    if len(wrapped_banner) > 1:
                        banner_line2 = wrapped_banner[1]
            if map_id:
                ascii_map_obj = map_manager.create_ascii_map(map_id, banner_line1, banner_line2)
                if ascii_map_obj:
                    rendered = ascii_map_obj.draw_map()
                    map_lines = rendered.split("\n")
                else:
                    map_lines = ["[Error loading Map]"]
            else:
                map_lines = ["No Map available"]

        print_three_column_screen(
            left_lines,
            middle_lines,
            map_lines,
            left_title="Game Menu",
            middle_title=middle_title,
            right_title="Map"
        )

        choice = input("Please select an option: ").strip().lower()
        if choice == "1":
            clear_screen()
            hero.showStats()
            input("Press Enter to continue...")
        elif choice == "2":
            look_around(hero)
        elif choice == "3":
            manage_inventory(hero)
        elif choice == "4" and not hero.current_building:
            enter_building(hero)
        elif choice == "5":
            talk_to_npc(hero)
        elif choice == "6":
            show_quest_log(hero)
        elif choice == "x" and hero.current_building:
            hero.current_building = None
            print("You exit the building and return to the open area.")
            input("Press Enter to continue...")
        elif choice == "c":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")


def game_loop(hero) -> None:
    clear_screen()
    print("Type 'm' to open the game menu, or 'q' to quit.")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "m":
            open_game_menu(hero)
            clear_screen()
        elif command == "q":
            print("Quitting game. Goodbye.")
            break
        else:
            print("Unknown command. Type 'm' for menu or 'q' to quit.")
