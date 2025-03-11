from initializeGame import create_new_game
from game_menu import game_loop

def main():


    hero = create_new_game()
    print("Welcome to TerminalRPG " + hero.name + "!")
    print("That's it so far, the game is still being worked on.")
    game_loop(hero)

if __name__ == "__main__":
    main()


