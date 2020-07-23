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
headers = ['Item ID', 'Brick Size', 'Brick Color', 'Brick Type', 'Item Type', 'Set Name', 'Piece Count', 'Price $', 'Quantity']

# Function that queries the DB to show store inventory 
def show_inventory():
    # Query the database
    cursor.execute('SELECT * FROM legoStore.dbo.items')

    # Put the data from the query into a list
    query_result = cursor.fetchall()
    block_inventory = [list(i) for i in query_result]

    # Print the data for individual blocks
    print("\n\nStore Inventoryt")
    print(tabulate(block_inventory, headers, floatfmt=".2f"))

# Function that has conditionals to identify which characteristic the user is searching for and allows them to provide details
def get_details(characteristic):
    details = [0] * 2
    characteristic.lower()
    if characteristic == "item id":
        details[0] = "ItemID"
        details[1] = input('Enter the ID number you are searching for: ')
        print("\n\nShowing results for Item ID " + details[1] + "\n\n")
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
    query = ('SELECT * FROM legostore.dbo.items WHERE ' + query_from + " = " + '\'' + description + '\'')
    return query

# Function to check if the requested item is in stock, if item is not in stock, return new quantity request
def in_stock_check(ID, quantity_requested):
    # Grab the quantity available from the database
    cursor.execute('SELECT Quantity FROM legostore.dbo.items WHERE ItemID = ' + str(ID))
    result = cursor.fetchall()
    query_result = [list(i) for i in result]
    quantity_available = query_result[0][0]

    # Check if the quantity that has been requested is available
    while int(quantity_requested) > quantity_available:
        print("Sorry we only have " + str(quantity_available) + " in stock currently. ")
        buy_all = input('Would you like to purchase all of those that are in stock? y or n? ')
        buy_all.lower()
        if buy_all == 'y':
            quantity_requested = quantity_available
            print('Added to cart')
        else:
            quantity_requested = input('How many would you like to buy? ')
    

    return quantity_requested

# Function that builds the update query when a user buys an individual brick
#def subtract_from_brick_inventory(ID, quantity_requested):
    

#def subtract_from_set_inventory(ID, quantity):

# Function to add all blocks and sets to one cart for easy display 
'''def compile_cart(cart):
    query_result = []

    # Display all the blocks in the cart 
    print('These are all the blocks currently in your cart')
    for i in range(len(blocks_cart)):
        if cart[i][0]:
            query = ('SELECT BrickID, BrickSize, BrickColor, BrickPrice, BrickType FROM legostore.dbo.individual_lego_bricks WHERE BrickID = ' + '\'' +cart[i][0] + '\'')
            cursor.execute(query)
            result = cursor.fetchall()
            query_result += [list(i) for i in result]

    cart_block_headers = ['Item ID', 'Size', 'Color', 'Price', 'Type']
    print(tabulate(query_result, cart_block_headers, floatfmt='.2f'))

    # Display all the sets in the cart
    print('These are all the sets currently in your cart')
    for i in range(len(sets_cart)):
        select_query_builder('SetName', str(sets_cart[i][0]))'''


# Function to browse the current inventory
def browse():
    # Print the data for individual blocks and sets
    show_inventory()

# Function to search the inventory 
def search():
    # Print message to the user asking what they are searching for
    help_message = (
        "\n\nWhat would you like to search for? Type in one of the options listed below.\n"
        "- Item ID\n- Brick Size\n- Brick Color\n- Brick Type\n- Set Name\n"
    )   

    # Get the user input 
    characteristic = input(help_message)

    # Get description details from the user
    details = get_details(characteristic)

    # Build the search query, details[0] is the column header and details[1] is the attr the user is searching for 
    query = select_query_builder(str(details[0]), str(details[1]))
    
    # Execute the query and save to list for formatted printing
    cursor.execute(query)
    query_result = cursor.fetchall()
    search_results = [list(i) for i in query_result]

    # Print the search results
    if not search_results:
        print('There are no products in our inventory matching that search.')
    else:
        print(tabulate(search_results, headers, floatfmt=".2f"))

# Function that will be used when a user chooses to make a purchase
def purchase():
    # Make a 2D list in the form [[itemID, Quantity], [itemID, Quantity]]
    cart = [([0] * 2 ) for row in range(50)]

    # Loop getting input from the user on what they are looking to buy 
    buyMore = True
    i = 0
    j = 0

    while buyMore: 
        # Display the current inventory and ask the user to enter item id and quantity of what they would like to buy 
        show_all_blocks()
        print('Above is our current inventory of individual bricks')
        cart[i][0] = input('Please enter the Item ID of the item you\'d like to purchase: ')
        cart[i][1] = input('And the quantity you want to purchase: ')
        cart[i][1] = in_stock_check(blocks_cart[i][0],cart[i][1]) # Check if in stock, if not update quantity
        i += 1

        # Ask the user if he wants to keep buying items
        keep_buying = input('Would you like to add more to your cart? y or n:  ')
        if keep_buying == 'n':
            buyMore = False


    # Add all blocks and sets to one cart
    # compile_cart(blocks_cart, sets_cart)

    