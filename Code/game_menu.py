from ui_helpers import clear_screen, print_three_column_screen, print_framed
from manage_inventory import manage_inventory
from dialog_menu import talk_to_npc
from location_manager import LocationManager, travel_to_neighbor
from npc_manager import NPCManager
from map_manager import MapManager
import os
import json
from time_system import GameTime
import textwrap
from building_menu import enter_building

def attack_enemy_in_location(hero):
    from battle_system import Battle
    lm = LocationManager()
    npc_m = NPCManager()
    current_location = lm.locations.get(hero.current_location, {})
    hostile_npcs = []
    if "enemy_spawns" in current_location:
        spawn_manager = lm.spawn_managers.get(hero.current_location)
        if spawn_manager:
            wolf_count = spawn_manager.current_spawns.get("npc_wolf", 0)
            hostile_npcs.extend(["npc_wolf"] * wolf_count)
    else:
        if "npcs" in current_location:
            for npc_id in current_location["npcs"]:
                npc_data = npc_m.get_npc_data(npc_id)
                if npc_data.get("attitude", "").lower() == "hostile":
                    hostile_npcs.append(npc_id)
    if not hostile_npcs:
        print("No hostile enemies in this location.")
        input("Press Enter to continue...")
        return
    print("Enemies in this location:")
    for idx, npc_id in enumerate(hostile_npcs, start=1):
        enemy_name = npc_m.get_npc_name(npc_id)
        print(str(idx) + ". " + enemy_name)
    choice = input("Select enemy to attack or press Enter to cancel: ").strip()
    if not choice.isdigit():
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(hostile_npcs):
        print("Invalid selection.")
        input("Press Enter to continue...")
        return
    selected_npc_id = hostile_npcs[idx]
    npc_data = npc_m.get_npc_data(selected_npc_id)
    enemy = type("Enemy", (), {})()
    enemy.name = npc_data.get("name", selected_npc_id)
    enemy.health = npc_data.get("health", 50)
    enemy.max_health = npc_data.get("health", 50)
    enemy.stamina = npc_data.get("stamina", 50)
    enemy.max_stamina = npc_data.get("stamina", 50)
    enemy.attack = npc_data.get("attack", 10)
    enemy.xp_reward = npc_data.get("xp_reward", 100)
    enemy.gold_reward = npc_data.get("gold_reward", 10)
    enemy.drop_chance = npc_data.get("drop_chance", 0.3)
    enemy.drop_item = npc_data.get("drop_item", None)
    enemy.emoji = npc_data.get("emoji", "❓")
    with open(os.path.join(os.path.dirname(__file__), "../JSON/attacks.json"), "r", encoding="utf-8") as f:
        attack_data = json.load(f)
    game_time = GameTime()
    battle = Battle(hero, enemy, attack_data, game_time)
    result = battle.run()
    if result == "lost":
        print("You have been defeated. Returning to Darkwood Forest...")
        hero.current_location = "loc_darkwood_forest"
        input("Press Enter to continue...")

def look_around(hero):
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()
    loc = lm.locations.get(hero.current_location, {})
    if loc:
        print_framed(loc.get("name", hero.current_location) + " (" + loc.get("type", "Unknown") + ")")
        if "enemy_spawns" in loc:
            spawn_manager = lm.spawn_managers.get(hero.current_location)
            for enemy_id, count in spawn_manager.current_spawns.items():
                for _ in range(count):
                    print(" - " + npc_m.get_npc_name(enemy_id))
        if loc.get("npcs"):
            for npc in loc["npcs"]:
                print(" - " + npc_m.get_npc_name(npc))
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

def open_quest_log(hero):
    from ui_helpers import clear_screen, print_framed
    while True:
        clear_screen()
        print_framed("Quest Log")
        print("1. Active Quests")
        print("2. Completed Quests")
        print("Press Enter to return")
        choice = input("Choose an option: ").strip().lower()
        if choice == "":
            confirm = input("Press Enter to confirm return or type 'c' to cancel: ").strip().lower()
            if confirm == "":
                break
        elif choice == "1":
            clear_screen()
            print_framed("Active Quests")
            if not hero.quest_log.active_quests:
                print("No active quests.")
            else:
                for idx, quest in enumerate(hero.quest_log.active_quests, start=1):
                    print(str(idx) + ". " + quest.name)
                    print("   " + quest.description)
                    print("   Objectives:")
                    for obj in quest.objectives:
                        status = str(obj.current) + "/" + str(obj.required) if not obj.completed else "Completed"
                        print("   - " + obj.description + " [" + status + "]")
                    print()
            input("Press Enter to continue...")
        elif choice == "2":
            clear_screen()
            print_framed("Completed Quests")
            if not hero.quest_log.completed_quests:
                print("No completed quests.")
            else:
                for idx, quest in enumerate(hero.quest_log.completed_quests, start=1):
                    print(str(idx) + ". " + quest.name)
                    print("   " + quest.description)
            input("Press Enter to continue...")
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

def wait_turn_for_hero(hero, game_time):
    import time
    hours_input = input("How many hours do you want to wait? (1-24): ").strip()
    try:
        hours_to_wait = int(hours_input)
        if hours_to_wait < 1 or hours_to_wait > 24:
            print("Invalid number. Waiting for 1 hour by default.")
            hours_to_wait = 1
    except ValueError:
        print("Invalid input. Waiting for 1 hour by default.")
        hours_to_wait = 1
    from location_manager import LocationManager
    lm = LocationManager()
    for i in range(hours_to_wait):
        phase, current_time = game_time.wait_turn()
        if hero.current_location in lm.spawn_managers:
            current_round = game_time._calendar.day * 24 + game_time._calendar.hour
            lm.spawn_managers[hero.current_location].update_spawns(current_round)
        hero.heal(10)
        print("Hour " + str(i+1) + "/" + str(hours_to_wait) + ": Now " + phase + ", time: " + current_time)
        time.sleep(0.5)
    input("Press Enter to continue...")

def open_game_menu(hero, game_time):
    lm = LocationManager()
    current_loc_id = hero.current_location
    map_manager = MapManager()
    npc_m = NPCManager()
    if current_loc_id in lm.spawn_managers:
        current_round = game_time._calendar.day * 24 + game_time._calendar.hour
        lm.spawn_managers[current_loc_id].update_spawns(current_round)
    while True:
        clear_screen()
        if hero.current_building:
            left_lines = [
                "1. Show Stats",
                "2. Look around",
                "3. Manage Inventory Items",
                "4. Enter Building",
                "5. Engage with NPCs",
                "6. Quest Log",
                "w  Wait one turn",
                "",
                "",
                "Press Enter to return"
            ]
            middle_title = "Building"
            b_info = lm.buildings.get(hero.current_building, {})
            b_name = b_info.get("name", "Unknown Building")
            b_desc = b_info.get("description", "No description provided.")
            b_faction = b_info.get("faction", "Unknown")
            b_type = b_info.get("type", "Unknown")
            wrapped_desc = textwrap.wrap("Description: " + b_desc, width=40)
            middle_lines = [
                "Faction: " + b_faction,
                "Type: " + b_type
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
                "5. Engage with NPCs",
                "6. Quest Log",
                "7. Travel",
                "8. Tech Tree",
                "w  Wait one turn",
                "",
                "Press Enter to return"
            ]
            middle_title = "Location"
            loc_info = lm.locations.get(hero.current_location, {})
            loc_name = loc_info.get("name", "Unknown Location")
            loc_desc = loc_info.get("description", "No description provided.")
            loc_faction = loc_info.get("faction", "Unknown")
            loc_type = loc_info.get("type", "Unknown")
            wrapped_desc = textwrap.wrap("Description: " + loc_desc, width=40)
            middle_lines = [
                loc_name,
                "Faction: " + loc_faction,
                "Type: " + loc_type
            ]
            middle_lines.extend(wrapped_desc)
            current_time_str = game_time._calendar.current_time()
            middle_lines.append("")
            middle_lines.append("")
            middle_lines.append("")
            middle_lines.append("Time: " + current_time_str)
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
        if choice == "":
            confirm = input("Press Enter to confirm return or type 'c' to cancel: ").strip().lower()
            if confirm == "":
                break
        elif choice == "1":
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
            talk_to_npc(hero, game_time)
        elif choice == "6":
            open_quest_log(hero)
        elif choice == "7":
            travel_to_neighbor(hero, game_time)
        elif choice == "8":
            from tech_tree import TechTree
            tech_tree = TechTree()
            tech_tree.display_menu(hero)
        elif choice == "w":
            wait_turn_for_hero(hero, game_time)
            clear_screen()
        elif choice == "x" and hero.current_building:
            hero.current_building = None
            print("You exit the building and return to the open area.")
            input("Press Enter to continue...")
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

def game_loop(hero):
    game_time = GameTime()
    clear_screen()
    print("Type m to start the game or press q to quit.")
    while True:
        command = input("Command: ").strip().lower()
        if command == "m":
            open_game_menu(hero, game_time)
            clear_screen()
        elif command == "q":
            print("Game closed, byebye!")
            break
        else:
            print("Unknown command, press m or q.")
