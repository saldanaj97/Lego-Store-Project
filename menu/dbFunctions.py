import pyodbc
import random
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

# Global variable that will be used to keep track of the users cart while making a purchase
unformatted_cart = []

# Function to authenticate both users and employees with the database
def user_auth(info):
    logged_in = False

    # Query the correct table based on the type of user 
    if info[0] == 'employee':
        cursor.execute('SELECT * FROM legoStore.dbo.employees WHERE EmployeeID = ' + '\'' + info[1] + '\'' + 'AND EmpPassword = ' + '\'' + info[2] + '\'')
        query_result = cursor.fetchall()
        user = [list(i) for i in query_result]
        if not user:
            print('\nAccount with those credentials not found. Please try again. \n')
            return False
    elif info[0] == 'customer':
        cursor.execute('SELECT * FROM legoStore.dbo.customer WHERE Email = ' + '\'' + info[1] + '\'' + 'AND UserPassword = ' + '\'' + info[2] + '\'')
        query_result = cursor.fetchall()
        user = [list(i) for i in query_result]
        if not user:
            print('\nAccount with those credentials not found. Please try again. \n')
            return False

    # If we haven't returned back to home, the user has successfully logged in 
    print("Successfully logged in. ")
    logged_in = True
    return logged_in

# Function that allows users to register for an account 
def register_user():
    print('\n****** Account Registration ****** \n')
    f_name = input('First Name: ')
    l_name = input('Last Name: ')
    phone_num = input('Phone Number: ')
    email_addr = input('Email Address: ')
    home_addr = input('Home Address: ')
    password = input('Password: ')

    # Query to add a new user to the customers table
    customer_counter  = random.randrange(2, 100000, 2) # Increment the customer ID counter
    cursor.execute(
        'INSERT INTO customer (CustomerID, FirstName, LastName, PhoneNumber, Email, HomeAddress, UserPassword) '
        'VALUES (\'' + str(customer_counter) + '\',\'' + str(f_name) + '\',\'' + str(l_name) + '\',\'' + str(phone_num )+ '\',\'' + str(email_addr) + '\',\'' + str(home_addr) + '\',\'' + str(password) + '\')'
    )

    # made sure command gets executed
    cnx.commit()
    print('\nAccount Created. \n')

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

# Function that will be used to add items from list to cart individually
def list_to_cart(old_list, new_cart):
    for sublist in old_list:
        for item in sublist:
            new_cart.append(item)
    return new_cart

# Function to add all blocks and sets to one cart for easy display 
def update_cart(cart):
    query_result = []
    cart_ = []

    # Display all the blocks in the cart 
    print('\n\nThese are all the items currently in your cart:\n')
    query = ('SELECT * FROM legostore.dbo.items WHERE ItemID = ' + '\'' + cart[0] + '\'')
    cursor.execute(query)
    result = cursor.fetchall()
    query_result.append(list(i) for i in result)

    # Split the items in the list and add individually to cart_
    cart_ = list_to_cart(query_result, cart_)

    # Edit the quantity to display the user requested quantity
    cart_[0][8] = cart[1]

    return cart_

# Function to browse the current inventory
def browse():
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
    cart_items = []
    formatted_cart = []

    # Loop getting input from the user on what they are looking to buy 
    buyMore = True
    while buyMore: 
        show_inventory()
        print('\n\nAbove is our current store inventory')
        cart_items.append(input('Please enter the Item ID of the item you\'d like to purchase: '))
        cart_items.append(input('And the quantity you want to purchase: '))
        cart_items[1] = in_stock_check(cart_items[0],cart_items[1]) # Check if in stock, if not update quantity
        keep_buying = input('Would you like to add more to your cart? y or n:  ')
        unformatted_cart.append(update_cart(cart_items))
        if keep_buying == 'n':
            buyMore = False
        cart_items.clear()

    # Format the queries into readable data for the user and print
    formatted_cart = list_to_cart(unformatted_cart, formatted_cart)
    print(tabulate(formatted_cart, headers, floatfmt=".2f") + '\n\n') 

    checkout = input('Would you like to checkout? y or n:')
    if checkout == 'y':
        print('Okay checking out')

    