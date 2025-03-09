from dialog import Dialog
import time

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
        self.inventory = inventory

    def showInventory(self):
        print("👜 Inventory:")
        for slot, item in self.inventory.items():
            if item:
                print(f" - {slot}: {item.name}")
            else:
                print(f" - {slot}: [Empty]")
        print("-" * 40)

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
            choice = input("Choose an option (enter a number): ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(option_keys):
                    chosen_key = option_keys[choice - 1]
                    hero_name = kwargs.get("hero_name", "Hero")
                    answer_text = options[chosen_key]
                    Dialog.clear_screen()
                    print(f"{hero_name}:")
                    Dialog.show(answer_text)
                    Dialog.wait_for_input()
                    followup_data = None
                    if "followup" in conv_data:
                        followup_data = conv_data["followup"].get(chosen_key)
                    if followup_data:
                        followup_lines = [line.format(**kwargs) for line in followup_data.get("dialog", [])]
                        for line in followup_lines:
                            Dialog.clear_screen()
                            print(f"{self.name}:")
                            Dialog.show(line)
                            Dialog.wait_for_input()
                    return chosen_key
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
        return None
