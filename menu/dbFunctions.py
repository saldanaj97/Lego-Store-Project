import pyodbc
from tabulate import tabulate

# Values needed to connect to the backend database
cnx = pyodbc.connect(
    server="localhost",
    database="legoStore",
    user='sa',
    tds_version='7.4',
    password="Juan1997",
    port=1433,
    driver='/usr/local/lib/libtdsodbc.so'
)

# Headers used for formatting the results from the queries
individual_block_headers = ["Item ID", "Size", "Color", "Price($)", "In stock", "Type"]
set_headers = ["Set ID", "Name", "Piece Count", "In stock"]

# Function to browse the current inventory
def browse():
    # Query the database
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM legoStore.dbo.individual_lego_bricks')
    
    # Put the data from the query into a list
    query_result = cursor.fetchall()
    block_inventory = [list(i) for i in query_result]

    # Print the data for individual blocks
    print("\n\nIndividual Piece Inventory")
    print(tabulate(block_inventory,invdividual_block_headers, floatfmt=".2f"))

    # Query the database for the block set data
    cursor.execute('SELECT * FROM legoStore.dbo.lego_brick_sets')
    query_result = cursor.fetchall()
    set_inventory = [list(i) for i in query_result]

    # Print the data for the sets
    print("\n\nSet Inventory")
    print(tabulate(set_inventory,set_headers))
    print("\n\n")
    
# Function to search the inventory 
def search():
    # Print message to the user asking what they are searching for
    help_message = (
        "\n\nWhat would you like to search for? Type in one of the options listed below.\n"
        "- Brick ID\n- Brick Size\n- Brick Color\n- Brick Type\n- Set Name\n"
    )   

    # Get the user input 
    characteristic = input(help_message)

    # Get description details from the user
    if characteristic == "Brick ID" or characteristic == "brick id" or characteristic == "brick ID":
        query_from = "BrickID"
        description = input('Enter the ID number you are searching for: ')
        print("\n\nShowing results for Brick ID " + description + "\n\n")
    elif characteristic == "Brick Size" or characteristic == "brick size":
        query_from = "BrickSize"
        description = input('Enter the Brick size you are searching for: ')
        print("\n\nShowing results for pieces of size " +  description + "\n\n")
    elif characteristic == "Brick Color" or characteristic == "brick color":
        query_from = "BrickColor"
        description = input('Enter the Brick color you are searching for: ') 
        print("\n\nShowing results for bricks in the color " + description + "\n\n")     
    elif characteristic == "Brick Type" or characteristic == "brick type":
        query_from = "BrickType"
        description = input('Enter the Brick type you are searching for: ')
        print("\n\nShowing results for " + description + " bricks" + "\n\n")
    elif characteristic == "Set Name" or characteristic == "set name":
        query_from = "SetName" 
        description = input('Enter the name of the set you are searching for: ')
        print("\n\nShowing results for sets named " + description + "\n\n")
    else:
        print("\n\n*** This does not match any characteristics. Please try searching again. ***\n")

    # Piece together the user input to form a query for the Database
    cursor = cnx.cursor()

    # Check if the user wants to query the set table or individual block table and build query accordingly
    if query_from == 'SetName':
        query = ('SELECT * FROM legostore.dbo.lego_brick_sets WHERE ' + query_from + " = " + '\'' + description + '\'')
    else:
        query = ('SELECT * FROM legostore.dbo.individual_lego_bricks WHERE ' + query_from + " = " + '\'' + description + '\'')
    
    # Execute the query and save to list for formatted printing
    cursor.execute(query)
    query_result = cursor.fetchall()
    search_results = [list(i) for i in query_result]
    if not search_results:
        print('There are no products in our inventory matching that search.')
    elif query_from == 'SetName':
        print(tabulate(search_results, set_headers, floatfmt=".2f"))
    else:
        print(tabulate(search_results, individual_block_headers, floatfmt=".2f"))

    