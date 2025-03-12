import json
import os
import time
import msvcrt
import logging

logger = logging.getLogger(__name__)

class Dialog:
    @staticmethod
    def load_dialogues() -> dict:
        json_path = os.path.join(os.path.dirname(__file__), "../JSON/dialogues.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error("dialogues.json not found!")
            return {}
        except json.JSONDecodeError:
            logger.error("dialogues.json is corrupted!")
            return {}

    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show(text: str, delay: float = 0.01) -> None:
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
    def wait_for_input() -> None:
        input("\n▶️  Press Enter to continue")

    @staticmethod
    def play(dialogue) -> None:
        for line in dialogue:
            Dialog.clear_screen()
            Dialog.show(line)
            Dialog.wait_for_input()
