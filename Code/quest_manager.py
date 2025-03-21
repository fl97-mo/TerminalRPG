import json
import os
from quest import Quest
from location_manager import LocationManager
from npc_manager import NPCManager
class QuestManager:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = self.load_quests()

    def load_quests(self):
        file_path = os.path.join(os.path.dirname(__file__), "../JSON/quests.json")
        with open(file_path, "r") as f:
            data = json.load(f)

        return {qid: Quest({"id": qid, **qdata}) for qid, qdata in data["quests"].items()}

    def unlock_quest(self, quest_id):
        quest = self.available_quests.get(quest_id)
        if quest and quest.status == "locked":
            quest.status = "available"
            print(f"Quest unlocked: {quest.name}")

    def start_quest(self, quest_id):
        quest = self.available_quests.get(quest_id)
        if quest and quest.status in ["available", "locked"]:
            quest.status = "active"
            self.active_quests.append(quest)
            print(f"New Quest: {quest.name}")
            print(f" - {quest.description}")

    def complete_quest(self, quest, hero):
        if quest in self.active_quests:
            self.active_quests.remove(quest)
        quest.status = "completed"
        self.completed_quests.append(quest)
        self.apply_rewards(quest, hero)
        print(f"Quest Complete: {quest.name}")
        rewards = quest.rewards
        reward_components = []
        if rewards.get("gold", 0):
            reward_components.append(f"Gold: {rewards.get('gold')}")
        if rewards.get("xp", 0):
            reward_components.append(f"XP: {rewards.get('xp')}")
        if rewards.get("items", []):
            reward_components.append(f"Items: {', '.join(rewards.get('items'))}")
        print("Reward Received: " + " | ".join(reward_components))

    def apply_rewards(self, quest, hero):
        hero.gold += quest.rewards.get("gold", 0)
        hero.add_xp(quest.rewards.get("xp", 0))
        for item in quest.rewards.get("items", []):
            hero.addToBackpack(item)

    def check_triggers(self, trigger_type, hero, **kwargs):
        lm = LocationManager()
        nm = NPCManager()
        for quest in self.active_quests:
            if quest.update_progress(trigger_type, **kwargs):
                assigned_npc = quest.assigned_npc
                npc_location = "Unknown Location"
                for loc in lm.locations.values():
                    if "npcs" in loc and assigned_npc in loc["npcs"]:
                        npc_location = loc.get("name", "Unknown Location")
                        break
                npc_name = nm.get_npc_name(assigned_npc)
                print(f"Quest Update: {quest.name} objectives completed – return to {npc_name} in {npc_location} to claim your reward.")
