import os
import ast
import random

# Define the folder where the files will be saved
folder = 'Data'

# Create the folder if it doesn't exist
os.makedirs(folder, exist_ok=True)

# Define the file paths with the folder
random_data_file = os.path.join(folder, 'Random_Data.txt')

### Function that saves the value
def save_value(input_value, filename):
    with open(filename, 'w') as f:
        f.write(input_value)

### Function that loads the value whenever the program starts   
def load_value(filename): 
    try:
        with open(filename, 'r') as f:
            read = f.read()
        return ast.literal_eval(read)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

### Function to roll random item and rarity, and store them in a slot
def roll_and_store(catalog, filename):
    # List of rarity and item strings
    rarity_strings = ["Legendary", "Epic", "Rare", "Uncommon", "Common"]
    item_strings = ["Aura", "Potion", "Gear"]

    # Generate random rarity and item
    random_rarity = random.choice(rarity_strings)
    random_item = random.choice(item_strings)
    
    # Prepare the value pair
    new_values = {'rarity': random_rarity, 'name': random_item}
    print(f"Rolled item: {new_values['name']}, rarity: {new_values['rarity']}")

    # Determine slot name
    slot_number = len(catalog) + 1
    slot_name = f"Slot{slot_number}"

    if slot_number <= 10:
        catalog[slot_name] = new_values
        save_value(str(catalog), filename)
        print(f"Stored in {slot_name}. Current catalog: {catalog}")
    else:
        print("New item discarded.")
        # Hvnt code the part tht when it exceeds the 10th slot, it'll crash


### Main

# Load catalog from the file
catalog = load_value(random_data_file)
print('Loaded catalog:', catalog)

while True:
    user_input = input('Type "roll" to roll, or "showcatalog" to display catalog >> ').lower()

    if user_input == 'roll':
        roll_and_store(catalog, random_data_file)

    elif user_input == 'showcatalog':
        print("Current catalog:")
        for slot_name, values in catalog.items():
            print(f"{slot_name}: Item = {values['name']}, Rarity = {values['rarity']}")

    else:
        print('Unknown command...')

