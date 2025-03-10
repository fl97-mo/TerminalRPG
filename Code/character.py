from dialog import Dialog
import time
import re
from validations import get_validated_choice
from backpack import Backpack
from item import get_rarity_color, RESET_COLOR

ansi_escape_pattern = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def visible_length(text):
    no_ansi = ansi_escape_pattern.sub('', text)
    return len(no_ansi)


class Character:
    def __init__(self, name, health, stamina, attack, level, guild):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.attack = attack
        self.level = level
        self.guild = guild

    def showStats(self):
        print(f"Name:    {self.name}\n"
              f"Level:   {self.level}\n"
              f"Guild:   {self.guild}\n"
              f"Health:  {self.health} HP\n"
              f"Stamina: {self.stamina} SP\n"
              f"Attack:  {self.attack} AP\n")

class Character:
    def __init__(self, name, health, stamina, attack, level, guild):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.attack = attack
        self.level = level
        self.guild = guild

    def showStats(self):
        print(f"Name:    {self.name}\n"
              f"Level:   {self.level}\n"
              f"Guild:   {self.guild}\n"
              f"Health:  {self.health} HP\n"
              f"Stamina: {self.stamina} SP\n"
              f"Attack:  {self.attack} AP\n")


class Hero(Character):
    def __init__(self, name, health, stamina, attack, level, guild, inventory):
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

        self.inventory = inventory
        self.backpack = Backpack(capacity=20)

        self.gold = 50
        self.recalcStats()

    def recalcStats(self):
        total_attack = self.base_attack
        total_health_bonus = 0

        for slot_name, equipped_item in self.inventory.items():
            if equipped_item:
                if hasattr(equipped_item, "attack_value"):
                    total_attack += equipped_item.attack_value
                if hasattr(equipped_item, "health_bonus"):
                    total_health_bonus += equipped_item.health_bonus

        self.attack = total_attack
        self.max_health = self.base_health + total_health_bonus

        if self.health > self.max_health:
            self.health = self.max_health

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def consume_item(self, item):
        if hasattr(item, "is_consumable") and item.is_consumable:
            heal_val = getattr(item, "heal_value", 0)
            if heal_val > 0:
                self.heal(heal_val)
                print(f"You consumed {item.name} and healed {heal_val} HP!")
            else:
                print(f"You consumed {item.name} - no healing value found.")
        else:
            print("This item is not consumable!")

    def addToBackpack(self, item, quantity=1):
        return self.backpack.add_item(item, quantity)

    def removeFromBackpack(self, slot_index, quantity=1):
        return self.backpack.remove_item(slot_index, quantity)

    def equip_item(self, new_item, target_slot):
        old_item = self.inventory.get(target_slot)
        if old_item:
            success = self.backpack.add_item(old_item, 1)
            if not success:
                print("Not enough space in the backpack to swap items!")
                return False
        self.inventory[target_slot] = new_item

        self.recalcStats()
        return True

    def unequip_item(self, slot_name):
        old_item = self.inventory.get(slot_name)
        if not old_item:
            print(f"No item in slot '{slot_name}'.")
            return False

        success = self.backpack.add_item(old_item, 1)
        if not success:
            print("Backpack is full. Can't unequip.")
            return False

        self.inventory[slot_name] = None
        self.recalcStats()
        return True

    def showInventory(self):

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
            it = self.inventory.get(slotname)
            if it:
                color = get_rarity_color(it.rarity)
                item_name = f"{color}{it.name}{RESET_COLOR}"
            else:
                item_name = "(none)"
            equipment_lines.append(f"[{code}] {slotname}: {item_name}")

        def format_backpack_slot(idx):
            n = idx + 1
            if n < 10:
                return f"[{n}] "
            else:
                return f"[{n}]"

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
                        it = slot_data["item"]
                        qty = slot_data["quantity"]
                        color = get_rarity_color(it.rarity)
                        item_name_colored = f"{color}{it.name}{RESET_COLOR}"
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

        def pad_to_width(text, width):
                    vis_len = visible_length(text)
                    if vis_len < width:
                        return text + " " * (width - vis_len)
                    else:
                        return text

        def format_backpack_row(row_data):
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
            right_str = ""
            if i < rows:
                row_data = backpack_matrix[i]
                right_str = format_backpack_row(row_data)

            left_str = pad_to_width(left_str, eq_width)
            right_str = pad_to_width(right_str, bp_width)
            print(f"│{left_str}│{right_str}│")

        print("└" + "─" * eq_width + "┴" + "─" * bp_width + "┘")

class NPC(Character):
    def __init__(self, name, health, stamina, attack, level, guild, dialogues):
        super().__init__(name, health, stamina, attack, level, guild)
        self.dialogues = dialogues

    def talk(self, conversation, **kwargs):
        conv_key = str(conversation)
        conv_data = self.dialogues.get(conv_key)
        if not conv_data:
            print(f"{self.name} has no dialogue for conversation {conversation}.")
            return None
        lines = [line.format(**kwargs) for line in conv_data.get("dialog", [])]

        for line in lines:
            Dialog.clear_screen()
            print(f"{self.name}:")
            Dialog.show(line)
            Dialog.wait_for_input()

        options = conv_data.get("options")
        if options:
            print("\nOptions:")
            option_keys = list(options.keys())
            for idx, key in enumerate(option_keys, start=1):
                print(f"{idx}. {key}")
            choice = get_validated_choice(
                "Choose an option (enter a number): ",
                valid_options=range(1, len(option_keys)+1)
            )
            chosen_key = option_keys[choice - 1]
            hero_name = kwargs.get("hero_name", "Hero")
            answer_text = options[chosen_key]
            Dialog.clear_screen()
            print(f"{hero_name}:")
            Dialog.show(answer_text)
            Dialog.wait_for_input()
            followup_data = conv_data.get("followup", {}).get(chosen_key)
            if followup_data:
                followup_lines = [line.format(**kwargs) for line in followup_data.get("dialog", [])]
                for line in followup_lines:
                    Dialog.clear_screen()
                    print(f"{self.name}:")
                    Dialog.show(line)
                    Dialog.wait_for_input()
            return chosen_key
        return None
