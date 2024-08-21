### Converts strings to JSON file/Dictionary
import ast

### Save file
file_name = 'value.txt' #save file

### Function that saves the value
def save_value(input_value, filename):
    with open(filename, 'w') as f:
        f.write(input_value)

### Function that load the value whenever the program starts        
def load_value(filename): 
    with open(filename, 'r') as f:
        read = f.read()
    return read

### Retrieves and shows the value, if no values create a new file
try: 
    values = ast.literal_eval(load_value(file_name)) #
    print('Loaded values: ', values)
except: # Users first time, create new file instead
    print('Creating a new file...')
    values = {} 


while True:
    user_input = input('item / count / print? >> ')
    
    if user_input == 'count': # Updates 'count' value
        values['count'] = input('How many >>')
        save_value(str(values), file_name)
        print('Current values: ', values)
    
    elif user_input == 'item':
        values['item'] = input("What item? >>") # Updates 'item' value
        save_value(str(values),file_name)
        print('Current values:', values)
    
    elif user_input == 'print' : # Shows the value of 'count' and 'item'
        print(values['count'], values['item'])
    
    else:
        print('Unknown command...')

### Not a completed program since if user types print before inserting any values, it'll crash
### All comments are added by Lee Jun Yan for education purposes and proof of learning
### Source: https://www.youtube.com/watch?v=lFRMdGfo_XA