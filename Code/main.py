from initializeGame import create_new_game
from character import *

def main():
    hero = create_new_game()
    print(f"Welcome to TerminalRPG {hero.name}!")
    print(f"That's it so far, the game is still being worked on, "
        "but I hope you're just as excited about the result as I am. ")
    
    hero.showStats()

if __name__ == "__main__":
    main()
