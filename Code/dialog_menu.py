from ui_helpers import clear_screen
from location_manager import LocationManager
from npc_manager import NPCManager
from colors import Colors

def talk_to_npc(hero):
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
        print(str(idx) + ". " + npc_name)
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
    clear_screen()
    formatted_npc_name = Colors.color_text(npc_name, style_names="Bold")
    print(formatted_npc_name + ":")
    print("1. Thank you")
    print("c. Cancel")
    dialogue_choice = input("Choose dialogue option: ").strip().lower()
    if dialogue_choice == "1":
        clear_screen()
        print(hero.name + ": Thank you, " + npc_name + "!")
        input("Press Enter to continue...")
        clear_screen()
        print(npc_name + ": You're welcome, traveler. May fortune smile upon you.")
        input("Press Enter to continue...")
    else:
        print("Canceled.")
        input("Press Enter to continue...")
