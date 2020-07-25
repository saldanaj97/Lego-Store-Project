import pyodbc
import random
from tabulate import tabulate
from datetime import date

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

# Function that will run execute the query on the DB and return the results 
def run_query(query):
    cursor.execute(query)
    results = cursor.fetchall()
    query_results_list = [list(i) for i in results]

    return query_results_list

# Function to authenticate both users and employees with the database
def user_auth(info):
    # Set the logged in bool to false since user is not yet logged in and make the currrent user's id a global var so we can access it in other functions
    logged_in = False
    global CURRENT_USER_ID

    # Query the correct table based on the type of user 
    if info[0] == 'employee':
        cursor.execute('SELECT EmployeeID FROM legoStore.dbo.employees WHERE EmployeeID = ' + '\'' + str(info[1]) + '\'' + 'AND EmpPassword = ' + '\'' + str(info[2]) + '\'')
        query_result = cursor.fetchall()
        user = [list(i) for i in query_result]
        if not user:
            print('\nAccount with those credentials not found. Please try again. \n')
            return False
    elif info[0] == 'customer':
        cursor.execute('SELECT CustomerID FROM legoStore.dbo.customer WHERE Email = ' + '\'' + str(info[1]) + '\'' + 'AND UserPassword = ' + '\'' + str(info[2]) + '\'')
        query_result = cursor.fetchall()
        user = [list(i) for i in query_result]
        if not user:
            print('\nAccount with those credentials not found. Please try again. \n')
            return False
        else:
            CURRENT_USER_ID = user[0][0]

    # If we haven't returned back to home, the user has successfully logged in 
    print("Successfully logged in. ")
    logged_in = True
    return logged_in

# Function that allows users to register for an account 
def register_user():
    print('\n****** Account Registration ****** \n')
    f_name = input('First Name: ')
    l_name = input('Last Name: ')
    phone_num = input('Phone Number(no spaces): ')
    email_addr = input('Email Address: ')
    home_addr = input('Home Address: ')
    password = input('Password: ')

    # Query to add a new user to the customers table
    customer_counter  = random.randrange(2, 100000) # Give the customer a random ID number in the system
    cursor.execute(
        'INSERT INTO customer (CustomerID, FirstName, LastName, PhoneNumber, Email, HomeAddress, UserPassword) '
        'VALUES (\'' + str(customer_counter) + '\',\'' + str(f_name) + '\',\'' + str(l_name) + '\',\'' + str(phone_num )+ '\',\'' + str(email_addr) + '\',\'' + str(home_addr) + '\',\'' + str(password) + '\')'
    )

    # Made sure command gets executed so account gets created in the DB
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
    print("\n\nStore Inventory")
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


# Function that will parse the query results into a list of attributes for each item
def result_parser(query_result, item_list):
    for sublist in query_result:
        item_list.append(sublist)
    return item_list


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

# Function to make sure the user entered a valid card number
def card_num_check(card_num):
    valid_num = False
    while not valid_num:
        if len(card_num) < 16:
            card_num = input('Please enter a valid 16 digit card number with no spaces in between: ')
        else:
            valid_num = True
    return card_num

# Function to add get user input when adding a new card 
def add_new_card(CURRENT_USER_ID):
    name = input('Cardholder Name: ')
    card_num = input('Card Number: ')
    card_num = card_num_check(card_num)
    exp_date = input('Expiration Date: ')
    cvc = input('CVC: ')
    save_card = input('Do you want to save this card for faster checkout next time? y or n? ')
    print('Card has now been saved. ')
    split_card_num = [(card_num[i:i+4]) for i in range(0, len(card_num), 4)]                    # Split the card number into groups of 4
    if save_card:
        query = (
            'INSERT INTO card_payment(CustomerID, CardholderName, CardNumber, ExpDate, CVC, LastFour) '
            'VALUES (\''+ str(CURRENT_USER_ID) + '\',\'' + str(name) + '\',\'' + str(card_num) + '\',\'' + str(exp_date) + '\',\'' + str(cvc) +  '\',\'' + str(split_card_num[3]) + '\')'
        )
        cursor.execute(query)
    return split_card_num
    
# Function that checks if a user has a card on file, if not allows them to add one
def card_on_file(order_number, CURRENT_USER_ID):
    query = ('SELECT * FROM card_payment WHERE CustomerID = ' + '\'' + str(CURRENT_USER_ID) + '\'')
    query_result = run_query(query)

    # Check if there are any cards on file 
    if not query_result:
        print('You do not have any cards on file, please enter your card info: ')
        split_card_num = add_new_card(CURRENT_USER_ID)
        query = ('UPDATE orders SET CardUsed = ' + '\'' + str(split_card_num[3]) + '\' WHERE OrderID = ' + '\'' + str(order_number) + '\'')
    else:
        print('These are the last 4 digits of the cards you have on file: ')
        for i in range(len(query_result)):
            print(i+1, ')', query_result[i][5])                                                     # i + 1 so 0) will not be displyed to the user
        card_to_use = input('Would you like to use one of these cards? If so, just type the option number of the card ie. 1. If you would like to add a new card type \'new\'. ')
        if card_to_use == 'new' or card_to_use == 'New':
            split_card_num = add_new_card(CURRENT_USER_ID)
            query = ('UPDATE orders SET CardUsed = ' + '\'' + str(split_card_num[3]) + '\' WHERE OrderID = ' + '\'' + str(order_number) + '\'')
        else:
            card_to_use = int(card_to_use) - 1
            query = ('UPDATE orders SET CardUsed = ' + '\'' + str(query_result[int(card_to_use)][5]) + '\' WHERE OrderID = ' + '\'' + str(order_number) + '\'')

    # Add the card used to the order 
    cursor.execute(query)

    print('\n\n****** Your order has been placed. Thank you for your purchase! ******\n\n')
    return True

# Function to that drives the checkout 
def checkout_(formatted_cart, total, CURRENT_USER_ID, payment_method):
    # Get an random order number
    order_number  = random.randrange(2, 100000000)
    paid = False

    # Create the order first 
    query = (
        'INSERT INTO orders (OrderID, CustomerID, OrderDate, OrderTotal) '
        'VALUES (\''+ str(order_number) + '\',\'' + str(CURRENT_USER_ID) + '\',\'' + str(date.today()) + '\',\'' + str(total) + '\')'
    )
    cursor.execute(query)

    # Add items that are in the cart to the order_items table
    for i in range(len(formatted_cart)):
        query = (
            'INSERT INTO order_items (OrderID, ItemID, Quantity, Price) '
            'VALUES (\''+ str(order_number) + '\',\'' + str(formatted_cart[i][0]) + '\',\'' + str(formatted_cart[i][8]) + '\',\'' + str(formatted_cart[i][7]) + '\')'
        )
        cursor.execute(query)
    
    print('\n****** Payment ******\n')
    if payment_method == 'Card':
        paid = card_on_file(order_number, CURRENT_USER_ID)
    elif payment_method == 'Cash':
        query = ('UPDATE orders SET CardUsed = \'Cash\' WHERE OrderID = ' + '\'' + str(order_number) + '\'')
        paid = True

    # If the order was paid then push changes to the database and empty the cart 
    if paid:
        print('Paid')
        return True
        
# Function to display what each item in the order is 
def detailed_history(history_):
    # List to hold the item id's
    items = []
    item_details = []
    details_headers = ['Item ID', 'Brick Size', 'Brick Color', 'Brick Type', 'Item Type', 'Set Name', 'Set Piece Count']

    # Get all of the item id's from the order
    for i in range(len(history_)):
        items.append(history_[i][1])

    for i in range(len(items)):
        query = ('SELECT ItemID, BrickSize, BrickColor, BrickType, ItemType, SetName, SetPieceCount FROM items WHERE ItemID = ' + '\'' + str(items[i]) + '\'')
        query_result = run_query(query)
        item_details = result_parser(query_result, item_details) # Use this function to split up the query results 

    print(tabulate(item_details, details_headers))


# Function to get the customers ID number from the database
def get_customer_ID(phone_num):
    customer_details = []
    not_found = ''

    CURRENT_USER_ID = ''

    # Query the DB to check if the user has an account in the system, if so set the global user ID for this order
    query = ('SELECT CustomerID FROM customer WHERE PhoneNumber = ' + '\'' + str(phone_num) + '\'')
    query_result = run_query(query)

    # If the number was not found ask if they wanna try another number or make a new account
    if not query_result:
        not_found = input('An account with that phone number does not exist. Would you like to try another phone number or make a new account? Type either \'new\' or \'other\': ')
        not_found.lower()
    else:
        CURRENT_USER_ID = query_result[0][0]

    if not_found == 'other':
        phone_num = input('Enter new number to try: ')
        get_customer_ID(phone_num)
    elif not_found == 'new': 
        register_user()
        phone_num = input('Enter the number of the account: ')
        get_customer_ID(phone_num)
    else:
        return CURRENT_USER_ID

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
    search_results = run_query(query)

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

    # Calculate the cart total 
    total = 0.00
    for i in range(len(formatted_cart)):
        total += float(formatted_cart[i][7]) * float(formatted_cart[i][8])
    print('Cart total = ${:.2f}'.format(total))

    # Ask the user if he is ready to checkout yet
    checkout = input('Would you like to checkout? y or n: ')
    if checkout == 'y':
        paid = checkout_(formatted_cart, total, CURRENT_USER_ID, 'Card')
    else:
        paid = False 

    # Clear the cart if the last order was paid for 
    if paid:
        formatted_cart.clear()
        unformatted_cart.clear()

# Function to display the order history of the user
def order_history():
    # Headers for displaying the information in table format
    history_headers = ['Order Number', 'Customer ID', 'Order Date', 'Order Total', 'Last Four Digits of Card Used']
    order_item_headers = ['Order Number', 'Item ID', 'Quantity', 'Price']

    # Query the DB
    query = ('SELECT * FROM legostore.dbo.orders WHERE CustomerID = ' + '\'' + str(CURRENT_USER_ID) + '\'')
    history = run_query(query)

    # Display history if there have been any purchases
    if not history:
        print('You have no recent purchases. ')
    else:
        print('\n\n******* Purchase History *******')
        print(tabulate(history, history_headers, floatfmt='.2f'), '\n\n')

    # Ask the user if he wants more information 
    more_info = input('Do you want more information about an order? y or n: ')
    more_info.lower()
    if more_info == 'y':
        order_num = input('Please enter the order number you want more information about: ')
        query = ('SELECT * FROM legostore.dbo.order_items WHERE OrderID = ' + '\'' + str(order_num) + '\'')
        history_ = run_query(query)
        
        if not history_:
            print("There were no orders matching that order number. Please try again. ")
        else:
            print('Purchase history for order number: ', order_num, '\n\n')
            print(tabulate(history_, order_item_headers, floatfmt='.2f'), '\n')
            detailed_history(history_)
    else: 
        return 

# Function that will handle an employee making a sell (most of the code is copied from the purchase function but with changes to the prompts)
def sell():
    # Get input on what they are selling
    cart_items = []
    formatted_cart = []
    paid = False

    # Loop getting input from the employee 
    buyMore = True
    while buyMore: 
        show_inventory()
        cart_items.append(input('Please enter the Item ID of the item you\'re selling: '))
        cart_items.append(input('And the quantity: '))
        cart_items[1] = in_stock_check(cart_items[0],cart_items[1]) # Check if in stock, if not update quantity
        keep_buying = input('Would you like to add more to the cart? y or n:  ')
        unformatted_cart.append(update_cart(cart_items))
        if keep_buying == 'n':
            buyMore = False
        cart_items.clear()

    # Format the queries into readable data for the user and print
    formatted_cart = list_to_cart(unformatted_cart, formatted_cart)
    print(tabulate(formatted_cart, headers, floatfmt=".2f") + '\n\n') 

    # Calculate the cart total 
    total = 0.00
    for i in range(len(formatted_cart)):
        total += float(formatted_cart[i][7]) * float(formatted_cart[i][8])
    print('Cart total = ${:.2f}'.format(total))

    # Ask the user if he is ready to checkout yet
    checkout = input('Ready for checkout? y or n: ')
    checkout.lower() 
    if checkout == 'y':
        has_account = input('Does the customer have an account on file? y or n: ')
        if has_account == 'y':
            phone_num = input('What is the customers phone number(enter with no spaces or hypens)? ')
            CURRENT_USER_ID = get_customer_ID(phone_num)
        elif has_account == 'n':
            register_user()
            phone_num = input('What is the customers phone number(enter with no spaces or hypens)? ')
            CURRENT_USER_ID = get_customer_ID(phone_num)
        else:  
            print('Invalid input')
        payment_method = input('Cash or Card? ')                        # Allow the user to pay either cash or card since they are in store
        payment_method.lower()
        if payment_method == 'card':
            paid = checkout_(formatted_cart, total, CURRENT_USER_ID, 'Card')
        elif payment_method == 'cash':
            paid = checkout_(formatted_cart, total, CURRENT_USER_ID, 'Cash')
        else:
            print('Invalid input')
    elif checkout == 'n':
        paid = False
    else: 
        print('Invalid Input')

    # Clear the cart if the last order was paid for 
    if paid:
        formatted_cart.clear()
        unformatted_cart.clear()
