class TechTree:
    def __init__(self):
        self.options = {
            "1": {"name": "Health", "bonus": 10, "attribute": "base_health"},
            "2": {"name": "Attack", "bonus": 5, "attribute": "base_attack"},
            "3": {"name": "Stamina", "bonus": 10, "attribute": "base_stamina"}
        }

    def display_menu(self, hero):
        if hero.tech_points <= 0:
            input("No tech points available. Press Enter to return.")
            return
        
        while hero.tech_points > 0:
            print("\nTech Tree - Available Points:", hero.tech_points)
            print("1. Health (+10 Max HP)")
            print("2. Attack (+5 Attack Power)")
            print("3. Stamina (+10 Max Stamina)")
            print("Enter. Exit")
            
            choice = input("Choose: ").strip()
            
            if not choice:
                break
                
            if choice == "1":
                hero.base_health += 10
                hero.recalcStats()
                hero.tech_points -= 1
                print(f"New Max Health: {hero.max_health} HP")
                
            elif choice == "2":
                hero.base_attack += 5
                hero.recalcStats()
                hero.tech_points -= 1
                print(f"New Attack: {hero.attack} AP")
                
            elif choice == "3":
                hero.base_stamina += 10
                hero.recalcStats()
                hero.tech_points -= 1
                print(f"New Max Stamina: {hero.max_stamina} SP")
                
            else:
                print("Invalid choice")
                
            input("Press Enter to continue...")