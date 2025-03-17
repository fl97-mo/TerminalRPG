import time
import sys
import msvcrt
import random, sys
import os
import string
from item import ItemLoader
from location_manager import LocationManager
from colors import Colors
class Battle:
    def __init__(self, hero, enemy, attack_data, game_time):
        self.hero = hero
        self.enemy = enemy
        self.attack_data = attack_data
        self.defending = False
        self.game_time = game_time
    def display_interface(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        enemy_emoji = getattr(self.enemy, "emoji", "❓")
        player_emoji = getattr(self.hero, "emoji", "❓")
        print("=== Battle ===\n")
        print(f"Enemy: {self.enemy.name} {enemy_emoji}")
        print(f"HP: {self.enemy.health}/{self.enemy.max_health}   Stamina: {self.enemy.stamina}\n")
        print("-" * 40 + "\n")
        print(f"Player: {self.hero.name} {player_emoji}")
        print(f"HP: {self.hero.health}/{self.hero.max_health}   Stamina: {self.hero.stamina}\n")

    def choose_hero_action(self):
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Use Item")
        print("4. Flee")
        action = input("Your choice: ").strip()
        return action

    def choose_attack(self):
        print("Choose an attack:")
        options = list(self.attack_data["attacks"].values())
        for idx, atk in enumerate(options, start=1):
            print(f"{idx}. {atk['name']} (Base Damage: {atk['base_damage']}, Stamina: {atk['stamina_cost']})")
        choice = input("Select attack: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid selection, executing Standard Attack.")
            time.sleep(1)
            return options[0]
        return options[int(choice) - 1]
    def simulate_minigame(self):

        bar_length = 30

        def generate_random_color_pattern(total):
            colors = ["Red", "Green", "Gold"]
            full_pattern = []
            previous_color = None
            segments = total // 2
            for _ in range(segments):
                available = [c for c in colors if c != previous_color]
                chosen = random.choice(available)
                full_pattern.extend([chosen] * 2)
                previous_color = chosen
            return full_pattern

        full_pattern = generate_random_color_pattern(bar_length)
        print("Press Enter when the bar is in the GOLD area!")
        empty_bar = "[" + " " * bar_length + "]"
        print(empty_bar, end="")
        sys.stdout.flush()
        time.sleep(0.5)

        result_multiplier = 1.0
        start_time = time.time()
        duration = 2.0
        entered = False
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            progress = int((elapsed / duration) * bar_length)
            if progress > bar_length:
                progress = bar_length
            bar = ""
            for i in range(bar_length):
                if i < progress:
                    bar += Colors.color_text("█", color_name=full_pattern[i])
                else:
                    bar += " "
            print("\r[" + bar + "]", end="")
            sys.stdout.flush()
            time.sleep(0.05)
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\r':
                    entered = True
                    break
        print()
        if not entered:
            result_multiplier = 0.25
            print("No input detected! Punished with 0.25 multiplier.")
        else:
            color_at_position = full_pattern[progress - 1] if progress > 0 else full_pattern[0]
            if color_at_position == "Gold":
                result_multiplier = 2.0
            elif color_at_position == "Green":
                result_multiplier = 1.0
            else:
                result_multiplier = 0.5
            print(f"Timing multiplier: {result_multiplier}!")
        time.sleep(1)
        return result_multiplier

    def simulate_typing_minigame(self):
        letters = list(string.ascii_lowercase)
        letter1 = random.choice(letters)
        letter2 = random.choice(letters)
        while letter2 == letter1:
            letter2 = random.choice(letters)
        target_combo = letter1 + letter2

        print(f"Your target combo is: {target_combo}")
        print("Get ready!")
        for i in range(2, 0, -1):
            print(f"Starting in {i}...", end="\r")
            time.sleep(1)
        print("Go! Type the combo repeatedly:")

        start_time = time.time()
        duration = 3.0
        input_sequence = ""
        print("Start typing now (keys will be recorded instantly):")
        while time.time() - start_time < duration:
            if msvcrt.kbhit():
                ch = msvcrt.getch().decode('utf-8', errors='ignore')
                if ch.isalpha():
                    input_sequence += ch.lower()
        print("\nTime's up!")
        count = 0
        idx = 0
        while idx < len(input_sequence) - 1:
            if input_sequence[idx:idx+2] == target_combo:
                count += 1
                idx += 2
            else:
                idx += 1
        print(f"You typed '{target_combo}' {count} times.")
        if count >= 15:
            multiplier = 2.0
        elif count >= 10:
            multiplier = 1
        elif count >= 5:
            multiplier = 0.75
        else:
            multiplier = 0.5
        print(f"Typing multiplier: {multiplier}!")
        time.sleep(1)
        return multiplier
    def hero_attack(self, attack):
        if attack['id'] == "alphabet":
            multiplier = self.alphabet_hero_attack()
        elif attack['id'] == "keycount":
            multiplier = self.simulate_typing_minigame()
        elif attack['id'] == "standard":
            multiplier = 1.0
        else:
            multiplier = self.simulate_minigame()
        damage = (attack['base_damage'] + self.hero.attack) * multiplier
        if self.hero.stamina < attack['stamina_cost']:
            print("Not enough stamina for this attack!")
            time.sleep(1)
            return 0
        self.hero.stamina -= attack['stamina_cost']
        print(f"You use {attack['name']} and deal {damage} damage!")
        time.sleep(1)
        return damage

    def alphabet_hero_attack(self):
        success_count = 0
        letters = string.ascii_lowercase
        print("Type the target letters!")
        print("Get ready!")
        for i in range(2, 0, -1):
            print(f"Starting in {i}...", end="\r")
            time.sleep(1)
        
        for i in range(5):
            target = random.choice(letters)
            print(f"Target letter: {target}")
            start_time = time.time()
            end_time = start_time + 1.0
            pressed = None
            
            while time.time() < end_time:
                if msvcrt.kbhit():
                    if pressed is None:
                        pressed = msvcrt.getch().decode("utf-8", errors="ignore").lower()
                time.sleep(0.01)
            if pressed is None:
                print(Colors.color_text("Fail (no input)", "Red"))
            elif pressed == target:
                print(Colors.color_text("Success", "Green"))
                success_count += 1
            else:
                print(Colors.color_text("Fail", "Red"))
            time.sleep(0.7)

        print(f"You got {success_count} correct out of 5!")
        if success_count >= 4:
            multiplier = 2.0
        elif success_count >= 2:
            multiplier = 1.0
        else:
            multiplier = 0.5
        print(f"Typing multiplier: {multiplier}!")
        time.sleep(1)
        return multiplier

    def enemy_attack(self):
        damage = self.enemy.attack
        if self.enemy.stamina < 5:
            print(f"{self.enemy.name} does not have enough stamina to attack!")
            return 0
        self.enemy.stamina -= 5
        print(f"{self.enemy.name} attacks and deals {damage} damage!")
        time.sleep(1)
        return damage

    def run(self):
        while self.hero.health > 0 and self.enemy.health > 0:
            self.display_interface()
            action = self.choose_hero_action()
            if action == "1":
                attack = self.choose_attack()
                dmg = self.hero_attack(attack)
                self.enemy.health -= dmg
                if self.enemy.health < 0:
                    self.enemy.health = 0
            elif action == "2":
                self.defending = True
                print("You assume a defensive stance.")
                time.sleep(1)
            elif action == "3":
                print("Item usage not implemented yet.")
                time.sleep(1)
            elif action == "4":
                print("Attempting to flee...")
                time.sleep(1)
                if random.random() < 0.5:
                    print("Flee successful!")
                    return "fled"
                else:
                    print("Flee failed!")
                    time.sleep(1)
            else:
                print("Invalid action, please choose again.")
                time.sleep(1)
                continue
            phase, current_time = self.game_time.wait_turn()
            print(f"Combat complete. Current time: {current_time} (Phase: {phase})")
            if self.enemy.health > 0:
                self.display_interface()
                enemy_dmg = self.enemy_attack()
                if self.defending:
                    shield_block = 5
                    enemy_dmg = max(0, enemy_dmg - shield_block)
                    print(f"Your defense reduces the damage by {shield_block}!")
                    self.defending = False
                    time.sleep(1)
                self.hero.health -= enemy_dmg
                if self.hero.health < 0:
                    self.hero.health = 0

            self.hero.stamina = min(self.hero.max_stamina, self.hero.stamina + 2)
            self.enemy.stamina = min(self.enemy.max_stamina, self.enemy.stamina + 2)

        if self.hero.health <= 0:
            print("You have been defeated!")
            time.sleep(2)
            return "lost"
        elif self.enemy.health <= 0:
            print(f"You have defeated {self.enemy.name}!")
            self.handle_rewards()
            lm = LocationManager()
            current_loc_id = self.hero.current_location
            if current_loc_id in lm.spawn_managers:
                lm.spawn_managers[current_loc_id].enemy_defeated("npc_wolf")
            return "won"

    def handle_rewards(self):
            xp_reward = getattr(self.enemy, "xp_reward", 50)
            gold_reward = getattr(self.enemy, "gold_reward", 10)
            print(f"You receive {xp_reward} XP!")
            self.hero.add_xp(xp_reward)
            if isinstance(gold_reward, dict):
                gold = random.randint(gold_reward.get("min", 0), gold_reward.get("max", 0))
            else:
                gold = gold_reward
            print(f"You receive {gold} Gold!")
            self.hero.gold += gold
            drop_chance = getattr(self.enemy, "drop_chance", 0.3)
            if random.random() < drop_chance:
                drop_item = getattr(self.enemy, "drop_item", None)
                if drop_item:
                    print(f"You have obtained {drop_item}!")
                    items = ItemLoader.load_items_from_json()
                    if drop_item in items:
                        self.hero.addToBackpack(items[drop_item])
            input("Press Enter to continue...")
