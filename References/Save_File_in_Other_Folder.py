import os 
 
### Define the path to the folder where you want to create the file 
folder_path = '/path/to/folder' 
 
### Create the folder if it doesn't exist 
if not os.path.exists(folder_path): 
    os.makedirs(folder_path) 
 
### Define the file name and path 
file_name = 'example.txt' 
file_path = os.path.join(folder_path, file_name) 
 
### Create the file 
with open(file_path, 'w') as f: 
    f.write('This is an example file.') 

### All comments are added by Lee Jun Yan for education purposes and proof of learning
### Source: https://www.quora.com/How-do-you-create-a-file-inside-another-folder-using-Python
