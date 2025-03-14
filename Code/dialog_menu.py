from ui_helpers import clear_screen, print_framed
from location_manager import LocationManager
from npc_manager import NPCManager
from colors import Colors
from validations import get_validated_choice
from character import Hero


def handle_quests(npc, hero, available_quests):
    clear_screen()
    print(f"{npc.name}'s Available Quests:")
    for idx, quest in enumerate(available_quests, 1):
        print(f"{idx}. {quest.name}")
    print("c. Cancel")

    choice = input("Choose quest: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(available_quests):
            quest = available_quests[idx]
            print(f"\n{quest.name}")
            print(f"{quest.description}")
            accept = input("Accept quest? (y/n): ").lower()
            if accept == "y":
                hero.quest_log.start_quest(quest.id)
def handle_quest_interaction(npc_id: str, hero: Hero) -> None:
    npc_manager = NPCManager()
    quest_manager = hero.quest_log
    available_quests = [q for q in quest_manager.available_quests.values() 
                        if q.assigned_npc == npc_id and not q.is_accepted]
    completable_quests = [q for q in quest_manager.active_quests 
                          if q.assigned_npc == npc_id and q.is_completed]

    while True:
        clear_screen()
        print_framed("Quest Options")
        options = []
        if available_quests:
            options.append(("1", "Available Quests"))
        if completable_quests:
            options.append(("2", "Complete Quests"))
        options.append(("c", "Back"))
        for key, text in options:
            print(f"{key}. {text}")
        choice = input("Choose option: ").strip().lower()

        if choice == "1" and available_quests:
            clear_screen()
            print_framed("Available Quests")
            for idx, quest in enumerate(available_quests, start=1):
                print(f"{idx}. {quest.name}")
                print(f"   {quest.description}")
                print("   Objectives:")
                for obj in quest.objectives:
                    print(f"   - {obj.description}")
                print()
            quest_choice = input("Choose quest to accept (number) or c to cancel: ").strip()
            if quest_choice.isdigit():
                idx = int(quest_choice) - 1
                if 0 <= idx < len(available_quests):
                    quest = available_quests[idx]
                    accept = input(f"Accept '{quest.name}'? (y/n): ").lower()
                    if accept == "y":
                        quest_manager.start_quest(quest.id)
                        print(f"Quest accepted: {quest.name}")
                        input("Press Enter to continue...")

        elif choice == "2" and completable_quests:
            clear_screen()
            print_framed("Complete Quests")
            for idx, quest in enumerate(completable_quests, start=1):
                print(f"{idx}. {quest.name}")
                print(f"   {quest.description}\n")
            quest_choice = input("Choose quest to complete (number) or c to cancel: ").strip()
            if quest_choice.isdigit():
                idx = int(quest_choice) - 1
                if 0 <= idx < len(completable_quests):
                    quest = completable_quests[idx]
                    quest_manager.complete_quest(quest, hero)
                    input("Press Enter to continue...")

        elif choice == "c":
            break

def talk_to_npc(hero: Hero) -> None:
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()

    location = lm.locations.get(hero.current_location)
    if not location or not location.get("npcs"):
        print("There is no one to talk to here.")
        input("Press Enter to continue...")
        return

    print("People here:")
    npc_list = location["npcs"]

    for idx, npc_id in enumerate(npc_list, start=1):
        npc_name = npc_m.get_npc_name(npc_id)
        print(f"{idx}. {npc_name}")
    print("c. Cancel")

    choice = input("Choose a person to talk to: ").strip().lower()

    if choice == "c":
        return

    if not choice.isdigit():
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(npc_list):
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    chosen_npc_id = npc_list[idx]
    npc_name = npc_m.get_npc_name(chosen_npc_id)

    while True:
        clear_screen()
        print_framed(npc_name)
        print("1. Talk")
        print("2. Quests")
        print("c. Cancel")
        
        action = input("Choose option: ").strip().lower()
        
        if action == "1":
            clear_screen()
            # Direkte Dialogimplementierung ohne handle_dialog
            print(f"{npc_name}:")
            print("1. Thank you")
            print("2. Quests")
            print("c. Cancel")
            
            dialog_choice = input("Choose dialogue option: ").strip().lower()
            if dialog_choice == "1":
                clear_screen()
                print(f"{hero.name}: Thank you, {npc_name}!")
                input("Press Enter to continue...")
                clear_screen()
                print(f"{npc_name}: You're welcome, traveler. May fortune smile upon you.")
                input("Press Enter to continue...")
        
        elif action == "2":
            handle_quest_interaction(chosen_npc_id, hero)
        
        elif action == "c":
            break
        
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()

    location = lm.locations.get(hero.current_location)
    if not location or not location.get("npcs"):
        print("There is no one to talk to here.")
        input("Press Enter to continue...")
        return

    print("People here:")
    npc_list = location["npcs"]

    for idx, npc_id in enumerate(npc_list, start=1):
        npc_name = npc_m.get_npc_name(npc_id)
        print(f"{idx}. {npc_name}")
    print("c. Cancel")

    choice = input("Choose a person to talk to: ").strip().lower()

    if choice == "c":
        return

    if not choice.isdigit():
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(npc_list):
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    chosen_npc_id = npc_list[idx]
    npc_name = npc_m.get_npc_name(chosen_npc_id)

    while True:
        clear_screen()
        print_framed(npc_name)
        print("1. Talk")
        print("2. Quests")
        print("c. Cancel")
        
        action = input("Choose option: ").strip().lower()
        
        if action == "1":
            clear_screen()
            print(f"{npc_name}:")
            print("1. Thank you")
            print("2. Quests")
            print("c. Cancel")
            
            dialog_choice = input("Choose dialogue option: ").strip().lower()
            if dialog_choice == "1":
                clear_screen()
                print(f"{hero.name}: Thank you, {npc_name}!")
                input("Press Enter to continue...")
                clear_screen()
                print(f"{npc_name}: You're welcome, traveler. May fortune smile upon you.")
                input("Press Enter to continue...")
        
        elif action == "2":
            handle_quest_interaction(chosen_npc_id, hero)
        
        elif action == "c":
            break
        
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()

    location = lm.locations.get(hero.current_location)
    if not location or not location.get("npcs"):
        print("There is no one to talk to here.")
        input("Press Enter to continue...")
        return

    print("People here:")
    npc_list = location["npcs"]

    for idx, npc_id in enumerate(npc_list, start=1):
        npc_name = npc_m.get_npc_name(npc_id)
        print(f"{idx}. {npc_name}")
    print("c. Cancel")

    choice = input("Choose a person to talk to: ").strip().lower()

    if choice == "c":
        return

    if not choice.isdigit():
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(npc_list):
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    chosen_npc_id = npc_list[idx]
    npc_name = npc_m.get_npc_name(chosen_npc_id)

    while True:
        clear_screen()
        print_framed(npc_name)
        print("1. Talk")
        print("2. Quests")
        print("c. Cancel")
        
        action = input("Choose option: ").strip().lower()
        
        if action == "1":
            clear_screen()
            print(f"{npc_name}:")
            print("1. Thank you")
            print("2. Quests")
            print("c. Cancel")
            
            dialog_choice = input("Choose dialogue option: ").strip().lower()
            if dialog_choice == "1":
                clear_screen()
                print(f"{hero.name}: Thank you, {npc_name}!")
                input("Press Enter to continue...")
                clear_screen()
                print(f"{npc_name}: You're welcome, traveler. May fortune smile upon you.")
                input("Press Enter to continue...")
        
        elif action == "2":
            handle_quest_interaction(chosen_npc_id, hero)
        
        elif action == "c":
            break
        
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
    clear_screen()
    lm = LocationManager()
    npc_m = NPCManager()

    location = lm.locations.get(hero.current_location)
    if not location or not location.get("npcs"):
        print("There is no one to talk to here.")
        input("Press Enter to continue...")
        return

    print("People here:")
    npc_list = location["npcs"]

    for idx, npc_id in enumerate(npc_list, start=1):
        npc_name = npc_m.get_npc_name(npc_id)
        print(f"{idx}. {npc_name}")
    print("c. Cancel")

    choice = input("Choose a person to talk to: ").strip().lower()

    if choice == "c":
        return

    if not choice.isdigit():
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(npc_list):
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    chosen_npc_id = npc_list[idx]
    npc_name = npc_m.get_npc_name(chosen_npc_id)

    while True:
        clear_screen()
        print_framed(npc_name)
        print("1. Talk")
        print("2. Quests")
        print("c. Cancel")
        
        action = input("Choose option: ").strip().lower()
        
        if action == "1":

            clear_screen()
            print(f"{npc_name}:")
            print("1. Thank you")
            print("2. Quests")
            print("c. Cancel")
            
            dialog_choice = input("Choose dialogue option: ").strip().lower()
            if dialog_choice == "1":
                clear_screen()
                print(f"{hero.name}: Thank you, {npc_name}!")
                input("Press Enter to continue...")
                clear_screen()
                print(f"{npc_name}: You're welcome, traveler. May fortune smile upon you.")
                input("Press Enter to continue...")
        
        elif action == "2":
            handle_quest_interaction(chosen_npc_id, hero)
        
        elif action == "c":
            break
        
        else:
            print("Invalid option.")
            input("Press Enter to continue...")