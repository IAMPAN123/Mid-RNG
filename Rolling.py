import random
import json
from Game.inventory import Inventory

def load_item_to_slot():
    """Load the item-to-slot mapping from a JSON file."""
    try:
        with open('Game/item_to_slot_count.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Handle file not found error
        return {}

item_to_slot_count = load_item_to_slot()

# Luck variables
Base = 1
UpgradeLuck = 0
EquipmentLuck = 0
MinigameLuck = 0
PotionLuck = 0
Bonus = 1
BonusRollCount = 0

# Luck Calculation
Luck = Base
if BonusRollCount == 10:
    Bonus = 2
elif BonusRollCount > 10:
    Bonus = 1
    BonusRollCount = 0

# Initialize inventory (or pass this object if already initialized elsewhere)
inventory = Inventory(screen=None)  # Assuming you're handling screen elsewhere

# Item rarity
Rarity = {
    'Common': 1, 'Uncommon': 2, 'Rare': 4, 'Epic': 8, 'Legendary': 10,
    'Mythic': 15, 'item6': 10, 'item7': 10, 'item8': 10, 'item9': 10,
    'item10': 8, 'item11': 8, 'item12': 8, 'item13': 8, 'item14': 8,
    'item15': 4, 'item16': 4, 'item17': 4, 'item18': 4, 'Malevolent': 100000000,
}

# Rolling Calculation
def FinalChance(Chance, Luck, Bonus):
    RollChance = Chance * ((Luck * Bonus))
    return RollChance

# Rolling System
run = True

# Uncomment and use this part for interactive rolling
# while run:
#     userinput = input()
#     if userinput == 'roll':
#         for x in Rarity:
#             NotActualFinalChance = (FinalChance(1 / Rarity[x], Luck, Bonus))
#             ActualFinalChance = 1 / NotActualFinalChance
#             try:
#                 Result = random.randint(1, int(ActualFinalChance))
#                 if Result == 1:
#                     print(x)
#                     BonusRollCount += 1
#                     if BonusRollCount == 10:
#                         Bonus = 2
#                     elif BonusRollCount > 10:
#                         Bonus = 1
#                         BonusRollCount = 0
#                     break
#                 else:
#                     continue
#             except ValueError:
#                 print('ValueError')
#     elif userinput == 'exit':
#         run = False
#     else:
#         print('Input error')
