def get_validated_name(prompt="Please enter your hero's name: ") -> str:
    while True:
        name = input(prompt).strip()
        if not name:
            print("The name cannot be empty. Please try again.")
        elif not name.replace(" ", "").isalpha():
            print("The name must contain only alphabetical characters. Please try again.")
        else:
            # Erlaubt auch mehrere Worte und formatiert jeden Teil
            name = " ".join(part.capitalize() for part in name.split())
            while True:
                confirm = input(f"Are you sure you want to be called {name}? You won't be able to change it later (y/n): ").strip().lower()
                if confirm == 'y':
                    return name
                elif confirm == 'n':
                    print("Alright, let's try again.")
                    break
                else:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def get_validated_choice(prompt="Please choose an option (number): ", valid_options=None) -> int:
    while True:
        choice = input(prompt).strip()
        if not choice.isdigit():
            print("Invalid input. Please enter only numbers.")
        else:
            num = int(choice)
            if valid_options and num not in valid_options:
                print(f"Invalid selection. Please choose one of the following options: {list(valid_options)}")
            else:
                return num
