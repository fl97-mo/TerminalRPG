# 🏹 TerminalRPG 🏰
👷‍♀️ **Under Construction!** 👷‍♂️  
A terminal-based RPG adventure. Currently in development! 

## About the Project
TerminalRPG is a medieval **text-based role-playing game** that runs in the terminal.  
The goal is to create an **interactive world** where players can:
- Explore the **world** 🏘️
- Engage in **battles** ⚔️
- Interact with **NPCs** 👩‍🌾
- Gain experience and get stronger over time 💪

## 🧙 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/fl97-mo/TerminalRPG.git
2. Navigate to the project folder:
   ```bash
   cd TerminalRPG
3. Run the game:
   ```bash
   python main.py


## 🧾 Dev Diary
### Day 3:
Created: 
- **`validations.py`**:       Input validations for different scenarios
- **`menu.py`**:              Prints and manages different menu options
- **`backpack.py`**:          Manages backpack logic

Implemented:

✅ **Inventory management**
- Hero can equip/dequip/consume/discard/inspect items
- When equiped/consumed items give specific bonuses
- Two Systems: 1. **Equipment** 2. **Backpack**
- Euipment: Weapons, armors, etc. can only be equiped at defined place.
- Backpack: Storage for all non equiped items. 20 Slots Max.
- Some items are stackable (up to 64), some are not 

### Day 2:
Created: 
- **`initializeGame.py`**:    Handles the game initializing and the intro.
- **`dialog.py`**:            Methods to display dialogs in RPG Styles
- **`dialogues.json`**:       Contains all dialogs and options to response.

Implemented:

✅ **Logic for NPC conversation with those scenarios:**
- NPC talks in monologue
- NPC asks for user input
- NPC reacts to user input

### Day 1:
Created: 
- **`main.py`**:              Controls the game logic.
- **`character.py`**:         Represents all characters.
- **`item.py`**:              Represent all items.
- **`items.json`**:           Contains all created items.

Implemented:

✅ **Creation of Item Objects and Hero Object (Player)**

