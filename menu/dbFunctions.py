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
# Cursor that will be used to query to DB
cursor = cnx.cursor()

# Headers used for formatting the results from the queries
individual_block_headers = ["Item ID", "Size", "Color", "Price($)", "In stock", "Type"]
set_headers = ["Set ID", "Name", "Piece Count", "In stock"]

# Function that queries the DB to show all individual bricks
def show_all_blocks():
    # Query the database
    cursor.execute('SELECT * FROM legoStore.dbo.individual_lego_bricks')

    # Put the data from the query into a list
    query_result = cursor.fetchall()
    block_inventory = [list(i) for i in query_result]

    # Print the data for individual blocks
    print("\n\nIndividual Piece Inventory")
    print(tabulate(block_inventory,individual_block_headers, floatfmt=".2f"))

# Function that queries the DB to show all available sets
def show_all_sets():
    # Query the database for the block set data
    cursor.execute('SELECT * FROM legoStore.dbo.lego_brick_sets')
    query_result = cursor.fetchall()
    set_inventory = [list(i) for i in query_result]

    # Print the data for the sets
    print("\n\nSet Inventory")
    print(tabulate(set_inventory,set_headers))
    print("\n\n")

# Function that has conditionals to identify which characteristic the user is searching for and allows them to provide details
def get_details(characteristic):
    details = [0] * 2
    characteristic.lower()
    if characteristic == "brick id":
        details[0] = "BrickID"
        details[1] = input('Enter the ID number you are searching for: ')
        print("\n\nShowing results for Brick ID " + details[1] + "\n\n")
    elif characteristic == "brick size":
        details[0] = "BrickSize"
        details[1] = input('Enter the Brick size you are searching for: ')
        print("\n\nShowing results for pieces of size " +  details[1] + "\n\n")
    elif characteristic == "brick color":
        details[0]= "BrickColor"
        details[1] = input('Enter the Brick color you are searching for: ') 
        print("\n\nShowing results for bricks in the color " + details[1] + "\n\n")     
    elif characteristic == "brick type":
        details[0] = "BrickType"
        details[1] = input('Enter the Brick type you are searching for: ')
        print("\n\nShowing results for " + details[1] + " bricks" + "\n\n")
    elif characteristic == "set name":
        details[0] = "SetName" 
        details[1] = input('Enter the name of the set you are searching for: ')
        print("\n\nShowing results for sets named " + details[1] + "\n\n")
    else:
        print("\n\n*** This does not match any characteristics. Please try searching again. ***\n")
    return details

# Function that builds the select query that displays all columns in a table
def select_query_builder(query_from, description):
    if query_from == 'SetName':
        query = ('SELECT * FROM legostore.dbo.lego_brick_sets WHERE ' + query_from + " = " + '\'' + description + '\'')
    else:
        query = ('SELECT * FROM legostore.dbo.individual_lego_bricks WHERE ' + query_from + " = " + '\'' + description + '\'')
    return query

# Function to browse the current inventory
def browse():
    # Print the data for individual blocks and sets
    show_all_blocks()
    show_all_sets()
    
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
    details = get_details(characteristic)

    # Build the search query, details[0] is the column header and details[1] is the attr the user is searching for 
    query = select_query_builder(details[0], details[1])
    
    # Execute the query and save to list for formatted printing
    cursor.execute(query)
    query_result = cursor.fetchall()
    search_results = [list(i) for i in query_result]

    # Print the search results
    if not search_results:
        print('There are no products in our inventory matching that search.')
    elif details[0] == 'SetName':
        print(tabulate(search_results, set_headers, floatfmt=".2f"))
    else:
        print(tabulate(search_results, individual_block_headers, floatfmt=".2f"))

# Function that will be used when a user chooses to make a purchase
def purchase():
    # Help message for buying individual bricks
    brick_help_message = (
        "\n\nType in one of the options listed below to get started purchasing.\n"
        "- Brick ID\n- Brick Size\n- Brick Color\n- Brick Type\n"
    )

    set_help_message = (
        "\n\nWhat would you like to buy? Type in one of the options listed below to get started.\n"
        "- Set Name\n- Set Piece Count"
    )

    # Make a 2D list in the form [[itemID, Quantity], [itemID, Quantity]] for MAX 50 items
    blocks_cart = [([0] * 2) for row in range(50)]

    # 2D list in same form as blocks cart but only for a MAX of 10 sets
    sets_cart = [([0] * 2) for row in range(10)]

    # Loop getting input from the user on what they are looking to buy 
    buyMore = True
    i = 0
    j = 0
    while buyMore: 
        brickOrSet = input('First, are you looking to buy individual bricks or a set? ')
        brickOrSet.lower()
        if brickOrSet == 'bricks' or brickOrSet == 'brick':
            show_all_blocks()
            print('Above is our current inventory of individual bricks')
            blocks_cart[i][0] = input('Please enter the brick ID of the item you\'d like to purchase: ')
            blocks_cart[i][1] = input('And the quantity you want to purchase: ')
            i += 1
        elif brickOrSet == 'sets' or brickOrSet == 'set':
            show_all_sets()
            print('Above is our current inventory of sets')
            sets_cart[j][0] = input('Please enter the set ID of the item you\'d like to purchase: ')
            sets_cart[j][1] = input('And the quantity you want to purchase: ')
            j += 1
        else:
            print('Please enter a valid input. Either \'bricks\' or \'sets\' are accepted. ')
        
        # Ask the user if he wants to keep buying items
        keep_buying = input('Would you like to add more to your cart? y or n:  ')
        if keep_buying == 'n':
            buyMore = False


    