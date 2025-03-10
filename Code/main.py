from initializeGame import create_new_game
from menu import GameMenu

def main():
    hero = create_new_game()
    print(f"Welcome to TerminalRPG {hero.name}!")
    print("That's it so far, the game is still being worked on.")

    GameMenu.game_loop(hero)

if __name__ == "__main__":
    main()


