from ui_helpers import clear_screen, print_framed
from location_manager import LocationManager
from npc_manager import NPCManager
from character import Hero
from dialog import Dialog
from battle_system import Battle
from npc_manager import NPCManager
from character import NPC
from shop_manager import ShopManager, open_shop_menu
import os
import json

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

def talk_to_npc(hero, game_time):
    lm = LocationManager()
    npc_m = NPCManager()
    Dialog.clear_screen()
    location = lm.locations.get(hero.current_location)
    if not location or not location.get("npcs"):
        print("There is no one to talk to here.")
        input("Press Enter to return...")
        return
    print("Characters here:")
    if "enemy_spawns" in location:
        spawn_manager = lm.spawn_managers.get(hero.current_location)
        if spawn_manager:

            wolf_count = spawn_manager.current_spawns.get("npc_wolf", 0)
            npc_list = ["npc_wolf"] * wolf_count
        else:
            npc_list = location.get("npcs", [])
    else:
        npc_list = location.get("npcs", [])
    for idx, npc_id in enumerate(npc_list, start=1):
        npc_name = npc_m.get_npc_name(npc_id)
        print(f"{idx}. {npc_name}")
    print("Press Enter to return.")
    choice = input("Choose a person to talk to: ").strip().lower()
    if choice == "":
        confirm = input("Press Enter to confirm return or type 'c' to cancel: ").strip().lower()
        if confirm == "":
            return
    if not choice.isdigit() or (int(choice) - 1) not in range(len(npc_list)):
        print("Invalid choice.")
        input("Press Enter to return...")
        return
    chosen_npc_id = npc_list[int(choice) - 1]
    npc_data = npc_m.get_npc_data(chosen_npc_id)
    role = npc_data.get("role", "")
    shop_id = npc_data.get("shop_id", None)
    if npc_data.get("attitude", "").lower() == "hostile":
        clear_screen()
        print(f"{npc_m.get_npc_name(chosen_npc_id)} is hostile!")
        print("1. Attack")
        print("0. Return")
        hostile_choice = input("Choose an option: ").strip().lower()
        if hostile_choice == "1":
            enemy = type("Enemy", (), {})()
            enemy.name = npc_data.get("name", chosen_npc_id)
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

            battle = Battle(hero, enemy, attack_data, game_time)
            result = battle.run()
            if result == "lost":
                print("You have been defeated. Returning to Darkwood Forest...")
                hero.current_location = "loc_darkwood_forest"
        return

    dialogues = Dialog.load_dialogues()
    npc_dialogues = dialogues.get(npc_data.get("dialogue_id"), {})
    branch = "greeting"
    branch_data = npc_dialogues.get(branch, {})
    npc = NPC(npc_data.get("name", chosen_npc_id), 100, 100, 10, 1, None, npc_dialogues, npc_id=chosen_npc_id)
    speaker_npc = npc_m.get_npc_name(chosen_npc_id)
    speaker_hero = hero.name
    quest_log = hero.quest_log

    def play_dialog(lines, speaker):
        for text_line in lines:
            Dialog.clear_screen()
            print(speaker)
            Dialog.show(text_line)
            Dialog.wait_for_input()

    already_greeted = False

    while True:
        Dialog.clear_screen()
        if not already_greeted:
            greeting_lines = [line.format(hero_name=hero.name) for line in branch_data.get("dialog", [])]
            if greeting_lines:
                play_dialog(greeting_lines, speaker_npc)
            already_greeted = True


        all_options = branch_data.get("options", [])
        filtered_options = []
        for opt in all_options:
            if opt.get("id") == "leave":
                continue
            quest_id = opt.get("followup", {}).get("quest")
            if quest_id:
                quest_obj = quest_log.available_quests.get(quest_id)
                if quest_obj and quest_obj.status in ["active", "completed"]:
                    continue
            filtered_options.append(opt)

        print("\nDialogue Options:")
        for idx, opt in enumerate(filtered_options, start=1):
            print(f"{idx}. {opt.get('text')}")
        print("0. Return")

        completable = [q for q in quest_log.active_quests if q.assigned_npc == chosen_npc_id and q.check_completion()]
        if completable:
            print("r. Claim Reward")
        if role == "shopkeeper":
            print("s. Open Shop")
        choice2 = input("Choose an option: ").strip().lower()
        if choice2 == "" or choice2 == "0":
            break
        if choice2 == "s" and role == "shopkeeper":
            shop_manager = ShopManager()  
            shop_instance = shop_manager.get_shop(shop_id)
            if shop_instance:
                open_shop_menu(hero, shop_instance)
            continue
        elif choice2 == "r" and completable:
            quest = completable[0]
            npc_location = "Unknown Location"
            for loc in lm.locations.values():
                if "npcs" in loc and chosen_npc_id in loc["npcs"]:
                    npc_location = loc.get("name", "Unknown Location")
                    break
            Dialog.clear_screen()
            reward_lines = [f"Quest '{quest.name}' completed – return to {npc_m.get_npc_name(chosen_npc_id)} in {npc_location} to claim your reward."]
            play_dialog(reward_lines, speaker_npc)
            confirm = input("Press Enter to confirm claim or type 'c' to cancel: ").strip().lower()
            if confirm == "":
                quest_log.complete_quest(quest, hero)
                input("Press Enter to continue...")
                break
            else:
                input("Press Enter to continue the conversation...")
                continue
        elif choice2.isdigit():
            opt_index = int(choice2) - 1
            if opt_index < 0 or opt_index >= len(filtered_options):
                print("Invalid option.")
                input("Press Enter to try again...")
                continue
            selected_opt = filtered_options[opt_index]
            reply_text = [selected_opt.get("reply", "").format(hero_name=hero.name)]
            play_dialog(reply_text, speaker_npc)
            if "npc_followup" in selected_opt:
                lines = [line.format(hero_name=hero.name) for line in selected_opt["npc_followup"].get("dialog", [])]
                play_dialog(lines, speaker_npc)
            elif "hero_followup" in selected_opt:
                lines = [line.format(hero_name=hero.name) for line in selected_opt["hero_followup"].get("dialog", [])]
                play_dialog(lines, speaker_hero)
            if "followup" in selected_opt and "quest" in selected_opt["followup"]:
                followup_data = selected_opt["followup"]
                if "dialog" in followup_data:
                    lines = [line.format(hero_name=hero.name) for line in followup_data["dialog"]]
                    play_dialog(lines, speaker_npc)
                quest_id = followup_data["quest"]
                if quest_id in quest_log.available_quests and quest_log.available_quests[quest_id].status in ["locked", "available"]:
                    accept = input("Press Enter to accept the quest or type 'c' to decline: ").strip().lower()
                    if accept == "":
                        quest_log.start_quest(quest_id)
                        print("Quest accepted!")
                        input("Press Enter to continue...")
                    else:
                        print("Quest declined. You can try again later.")
                        input("Press Enter to continue the conversation...")
                        continue
            continue
        else:
            print("Invalid option.")
            input("Press Enter to try again...")
