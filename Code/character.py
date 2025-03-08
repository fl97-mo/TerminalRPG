class Character():

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
        for item in self.inventory.items():
            print(item)
