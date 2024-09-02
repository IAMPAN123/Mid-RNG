import os
import ast

# Define the folder where the files will be saved
folder = 'Data'

# Create the folder if it doesn't exist
os.makedirs(folder, exist_ok=True)

# Define the file paths with the folder
save_file = os.path.join(folder, 'save.txt')
catalog_file = os.path.join(folder, 'catalog.txt')

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

### Function to clear a specific value in the dictionary
def clear_value(values, filename):
    values.clear()
    save_value(str(values), filename)
    print("All values have been cleared. Current values:", values)

### Function that saves the value pair into inventory slot
def save_to_slot(slot_name, values, catalog, filename):
    # Save current values to a slot in the catalog
    catalog[slot_name] = values.copy()
    save_value(str(catalog), filename)
    print(f"Saved to slot '{slot_name}'. Current catalog: {catalog}")

### Function that deletes the value pair into inventory slot
def clear_slot(catalog, filename, slot_name):
    if slot_name in catalog:
        del catalog[slot_name]
        save_value(str(catalog), filename)
        print(f"Slot '{slot_name}' has been cleared. Current catalog: {catalog}")
    else:
        print(f"Slot '{slot_name}' does not exist in the catalog.")

# Load values and catalog from their respective files
values = load_value(save_file)
print('Loaded values: ', values)

catalog = load_value(catalog_file)
print('Loaded catalog: ', catalog)



### Main

while True:
    user_input = input('rarity/count/name/print/clear/clearslot/saveslot/showcatalog >> ').lower()
    
    if user_input == 'count': # Updates 'count' value
        values['count'] = input('How many >>')
        save_value(str(values), save_file)
        print('Current values: ', values)
    
    elif user_input == 'rarity': # Updates 'rarity' value
        values['rarity'] = input("What rarity? >>")
        save_value(str(values),save_file)
        print('Current values:', values)
        # Legendary, Epic, Rare, Uncommon, Commmon 

    elif user_input == 'name':
        values['name'] = input("Name of item? >>") # Updates 'name' value
        save_value(str(values),save_file)
        print('Current values:', values)
        # Aura, Gear, Potion 

    elif user_input == 'clear': # Deletes all stored values
        clear_value(values, save_file)

    elif user_input == 'saveslot': # Saves the current values into a slot in the catalog
        slot_name = input("Enter a name for this slot >> ")
        save_to_slot(slot_name, values, catalog, catalog_file)

    elif user_input == 'clearslot':  # Clear a specific slot in the catalog
        slot_name = input("Enter the name of the slot to clear >> ")
        clear_slot(catalog, catalog_file, slot_name)

    elif user_input == 'showcatalog': # Shows the current catalog with all slots
        print("Current catalog:", catalog)

    elif user_input == 'print': # Shows the value of 'count' 'name' 'rarity'
        rarity = values.get('rarity', 'No value set')
        name = values.get('name', 'No value set')
        count = values.get('count', 'No value set')
        print(f"count: {count}, name: {name}, rarity: {rarity}")
    
    else:
        print('Unknown command...')

### Text inputs will be replaced by buttons function soon

