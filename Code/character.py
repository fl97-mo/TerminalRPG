import re
from validations import get_validated_choice
from backpack import Backpack
from item import get_rarity_color, RESET_COLOR
from colors import Colors
from npc_manager import NPCManager
from dialog import Dialog
from quest_manager import QuestManager
ansi_escape_pattern = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def visible_length(text: str) -> int:
    return len(ansi_escape_pattern.sub('', text))

class Character:
    def __init__(self, name: str, health: int, stamina: int, attack: int, level: int, guild: str):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.attack = attack
        self.level = level
        self.guild = guild

    def showStats(self) -> None:
        hero_formatted = Colors.color_text(self.name, color_name="Cyan", style_names="Bold")
        print(f"Name:    {hero_formatted}\n"
              f"Level:   {self.level}\n"
              f"XP:      {self.current_xp}/{self.next_level_xp}\n"
              f"Guild:   {self.guild}\n"
              f"Health:  {self.health} HP\n"
              f"Stamina: {self.stamina} SP\n"
              f"Attack:  {self.attack} AP\n") 

class Hero(Character):
    def __init__(self, name: str, health: int, stamina: int, attack: int, level: int, guild: str, inventory: dict):
        super().__init__(name, health, stamina, attack, level, guild)
        self.base_health = health
        self.base_stamina = stamina
        self.base_attack = attack

        self.max_health = self.base_health
        self.max_stamina = self.base_stamina
        self.health = self.base_health
        self.stamina = self.base_stamina
        self.attack = self.base_attack

        self.level = level
        self.guild = guild
        self.current_building = None
        self.inventory = inventory
        self.backpack = Backpack(capacity=20)
        self.gold = 50
        self.recalcStats()
        self.current_xp = 0
        self.next_level_xp = self.calculate_xp_requirement()
        self.quest_log = QuestManager()
    def calculate_xp_requirement(self):
        base_xp = 100
        return int(base_xp * (1.5 ** (self.level)))

    def add_xp(self, amount):
        self.current_xp += amount
        print(f"Gained {amount} XP!")
        while self.current_xp >= self.next_level_xp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.current_xp -= self.next_level_xp
        self.next_level_xp = self.calculate_xp_requirement()
        print(f"New Level ({self.level}) reached!")
        self.base_health += 10
        self.base_attack += 2
        self.recalcStats()

 
    def recalcStats(self) -> None:
        total_attack = self.base_attack
        total_health_bonus = 0

        for slot_item in self.inventory.values():
            if slot_item:
                total_attack += getattr(slot_item, "attack_value", 0)
                total_health_bonus += getattr(slot_item, "health_bonus", 0)

        self.attack = total_attack
        self.max_health = self.base_health + total_health_bonus
        if self.health > self.max_health:
            self.health = self.max_health

    def heal(self, amount: int) -> None:
        self.health = min(self.health + amount, self.max_health)

    def consume_item(self, item) -> None:
        if getattr(item, "is_consumable", False):
            heal_val = getattr(item, "heal_value", 0)
            if heal_val > 0:
                self.heal(heal_val)
                print(f"You consumed {item.name} and healed {heal_val} HP!")
            else:
                print(f"You consumed {item.name} - no healing value found.")
        else:
            print("This item is not consumable!")

    def addToBackpack(self, item, quantity: int = 1) -> bool:
        return self.backpack.add_item(item, quantity)

    def removeFromBackpack(self, slot_index: int, quantity: int = 1) -> bool:
        return self.backpack.remove_item(slot_index, quantity)

    def equip_item(self, new_item, target_slot: str) -> bool:
        old_item = self.inventory.get(target_slot)
        if old_item:
            if not self.backpack.add_item(old_item, 1):
                print("Not enough space in the backpack to swap items!")
                return False
        self.inventory[target_slot] = new_item
        self.recalcStats()
        return True

    def unequip_item(self, slot_name: str) -> bool:
        old_item = self.inventory.get(slot_name)
        if not old_item:
            print(f"No item in slot '{slot_name}'.")
            return False
        if not self.backpack.add_item(old_item, 1):
            print("Backpack is full. Can't unequip.")
            return False
        self.inventory[slot_name] = None
        self.recalcStats()
        return True

    def showInventory(self) -> None:
        print(f"HP: {self.health}/{self.max_health} | "
              f"SP: {self.stamina} | "
              f"Attack: {self.attack} | "
              f"Level: {self.level} | "
              f"Gold: {self.gold}")
        eq_slots = [
            ("E1", "Head"),
            ("E2", "Armor"),
            ("E3", "Legs"),
            ("E4", "Boots"),
            ("E5", "Left Hand"),
            ("E6", "Right Hand"),
            ("E7", "Amulett"),
            ("E8", "Ring 1"),
            ("E9", "Ring 2")
        ]
        equipment_lines = []
        for code, slotname in eq_slots:
            item_obj = self.inventory.get(slotname)
            if item_obj:
                color = get_rarity_color(item_obj.rarity)
                item_name = f"{color}{item_obj.name}{RESET_COLOR}"
            else:
                item_name = "(none)"
            equipment_lines.append(f"[{code}] {slotname}: {item_name}")

        def format_backpack_slot(idx: int) -> str:
            n = idx + 1
            return f"[{n:2}]"

        rows = 10
        cols = 2
        backpack_matrix = []
        current_idx = 0
        for _ in range(rows):
            row_data = []
            for _ in range(cols):
                if current_idx < len(self.backpack.slots):
                    slot_data = self.backpack.slots[current_idx]
                    if slot_data:
                        item_obj = slot_data["item"]
                        qty = slot_data["quantity"]
                        color = get_rarity_color(item_obj.rarity)
                        item_name_colored = f"{color}{item_obj.name}{RESET_COLOR}"
                        row_data.append(f"{format_backpack_slot(current_idx)} {item_name_colored} x{qty}")
                    else:
                        row_data.append(f"{format_backpack_slot(current_idx)} (empty)")
                    current_idx += 1
                else:
                    row_data.append("(n/a)")
            backpack_matrix.append(row_data)

        eq_width = 40
        bp_width = 60
        col_slot_width = 28

        def pad_to_width(text: str, width: int) -> str:
            vis_len = visible_length(text)
            return text + " " * max(0, width - vis_len)

        def format_backpack_row(row_data) -> str:
            col1 = pad_to_width(row_data[0], col_slot_width)
            col2 = pad_to_width(row_data[1], col_slot_width)
            combined = col1 + col2
            return pad_to_width(combined, bp_width)

        print("┌" + "─" * eq_width + "┬" + "─" * bp_width + "┐")
        left_title = pad_to_width(" Equipment ", eq_width)
        right_title = pad_to_width(" Backpack ", bp_width)
        print(f"│{left_title}│{right_title}│")
        print("├" + "─" * eq_width + "┼" + "─" * bp_width + "┤")
        max_lines = max(len(equipment_lines), rows)
        for i in range(max_lines):
            left_str = equipment_lines[i] if i < len(equipment_lines) else ""
            right_str = format_backpack_row(backpack_matrix[i]) if i < rows else ""
            left_str = pad_to_width(left_str, eq_width)
            right_str = pad_to_width(right_str, bp_width)
            print(f"│{left_str}│{right_str}│")
        print("└" + "─" * eq_width + "┴" + "─" * bp_width + "┘")

class NPC(Character):
    def __init__(self, name: str, health: int, stamina: int, attack: int, level: int, guild: str, dialogues: dict, npc_id: str = None):
        super().__init__(name, health, stamina, attack, level, guild)
        self.dialogues = dialogues
        self.npc_id = npc_id

    def talk(self, conversation, **kwargs):
        conv_key = str(conversation)
        conv_data = self.dialogues.get(conv_key)
        if not conv_data:
            print(f"{self.name} has no dialogue for conversation {conversation}.")
            return None
        lines = [line.format(**kwargs) for line in conv_data.get("dialog", [])]
        if self.npc_id:
            npc_manager = NPCManager()
            speaker_name = npc_manager.get_npc_name(self.npc_id)
        else:
            speaker_name = Colors.color_text(self.name, color_name="Bright White", style_names="Bold")
        for line in lines:
            Dialog.clear_screen()
            print(f"{speaker_name}:")
            Dialog.show(line)
            Dialog.wait_for_input()
        options = conv_data.get("options")
        if options:
            print("\nOptions:")
            for idx, option in enumerate(options, start=1):
                print(f"{idx}. {option['text']}")
            choice = get_validated_choice("Choose an option (enter a number): ", valid_options=range(1, len(options)+1))
            chosen_option = options[choice - 1]
            hero_name = Colors.color_text(kwargs.get('hero_name', 'Hero'), color_name="Cyan", style_names="Bold")
            answer_text = chosen_option["reply"]
            Dialog.clear_screen()
            print(f"{hero_name}:")
            Dialog.show(answer_text)
            Dialog.wait_for_input()
            followup_data = chosen_option.get("followup")
            if followup_data:
                followup_lines = [line.format(**kwargs) for line in followup_data.get("dialog", [])]
                for line in followup_lines:
                    Dialog.clear_screen()
                    print(f"{speaker_name}:")
                    Dialog.show(line)
                    Dialog.wait_for_input()
                if "quest" in followup_data:
                    quest_id = followup_data["quest"]
                    quest_log = kwargs.get("hero").quest_log if "hero" in kwargs else None
                    if quest_log and quest_log.available_quests[quest_id].status == "locked":
                        quest_log.unlock_quest(quest_id)
                        start_now = input(f"Do you want to start the quest '{quest_log.available_quests[quest_id].name}' now? (y/n): ").lower()
                        if start_now == "y":
                            quest_log.start_quest(quest_id)
            return chosen_option["id"]
        return None
