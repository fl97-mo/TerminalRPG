import json
import os
import time
import msvcrt


class Dialog:
    @staticmethod
    def load_dialogues():
        json_path = os.path.join(os.path.dirname(__file__), "../JSON/dialogues.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("dialogues.json not found!")
            return {}


    @staticmethod
    def clear_screen():
        """Clears screen for dialogs"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show(text, delay=0.02):
        """Shows dialog letter by letter, but skips if Enter is pressed"""
        full_text = ""
        for char in text:
            if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                print(text[len(full_text):], end='', flush=True)
                break

            print(char, end='', flush=True)
            full_text += char
            time.sleep(delay)

        print()

    @staticmethod
    def wait_for_input():
        """Ask for enter to continue"""
        input("\n▶️ Press Enter to continue")

    @staticmethod
    def play(dialogue):
        """shows list of dialog with effects"""
        for line in dialogue:
            Dialog.clear_screen()
            Dialog.show(line)
            Dialog.wait_for_input()
