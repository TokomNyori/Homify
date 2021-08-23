from sys import argv, exit
from cs50 import SQL
from db_helper import insert_building, insert_type, deleteTables

# Command line argument checker | required two args
if not len(argv) == 2:
    print('Error: Input exactly one command line argument after the program name')
    exit()

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///home.db")

# Inserting into building table
if argv[1] == 'insert_building':
    image = input("Image: ")
    name = input("Name: ")
    position = input("Position: ")
    # calling insert_building function from db_helper
    insert_building(image, name, position, db)

# Inserting into type table
if argv[1] == 'insert_type':
    print("type...........ist")
    insert_type(db)

sqlTables = ['properties', 'bhk_types', 'bhk_details', 'facade_images','interiors', 'nearby', 'features', 'property_audios']

if argv[1] == 'delete':
    print("Deleting...")
    deleteTables(sqlTables, db)



