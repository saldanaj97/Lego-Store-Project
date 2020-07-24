from pytabby import Menu
import menu_configs
import pyfiglet
import dbFunctions

# Help text with instructions on how to use the app 
def print_help():
    help_text = (
        "\n\nThis app is used to manage a lego store.\n\nEmployees can select the store mode option and which will require "
        "the user to login to be able to access the options for store mode such as\n"
        "   - Selling an item\n"
        "   - Managing Orders\n"
        "   - Managing the inventory database\n\n"
        "Users can select online mode which will only require a login/account creation for ordering items "
        "and checking purchase history. Online mode functions include\n"
        "   - Browsing inventory\n"
        "   - Searching for a specific item\n"
        "   - Checking puchase history\n\n"

        "To get to store or online mode type in 'store' or 'online' and then you will be presented with options for that mode. \n\n"
        "In order to make a selection, enter the number of the option that contains the desired selection. \n\n"
        "To get out of the current mode, type 'main menu' from either mode and/or just type 'q' to quit the program. \n"

    )
    print(help_text)


# Info will hold the userType, id and the password in repsective indicies ie. [UserType, ID, Passwd]
INFO = [0,0,0]

# Function that prompts the user to login and runs the user authentication when login info has been entered
def login_prompt():
    IS_LOGGED_IN = False

    # Require the user to login and check if the login is valid
    print('\n****** Login ******\n')
    INFO[0] = input('Employee or Customer? ')
    while IS_LOGGED_IN == False:
        INFO[0].lower()
        if INFO[0] == 'employee':
            INFO[1] = input('Employee ID: ')
            INFO[2] = input('Password: ')
            IS_LOGGED_IN = dbFunctions.user_auth(INFO)
        elif INFO[0] == 'customer':
            INFO[1] = input('Email: ')
            INFO[2] = input('Password: ')
            IS_LOGGED_IN = dbFunctions.user_auth(INFO)
        else:
            INFO[0] = input("Invalid input. Are you an employee or customer?")



# Main loop for the app to run 
def main_loop(): 
    # Logic for the app
    menu = Menu(menu_configs.MAIN_MENU_CONFIG)
    store_name = pyfiglet.figlet_format("The Lego Store")
    quit_early = False

    # Prompt the user to login or register 
    print(store_name)
    has_account = input('Do you have an account with us? y or n? (You will need one to use our service) ')
    has_account.lower()
    if has_account == 'y':
        login_prompt()
    elif has_account == 'n':
        dbFunctions.register_user()
        login_prompt()

    # Display help text so user knows how to use the program 
    print_help()

    # Start the main menu loop
    while not quit_early: 
        print(store_name)
        result = menu.run(message={"store": "You are in store mode.", "online": "You are in online mode."})
        if result[1] == "help":
            print_help()
        elif result[0] == "store" and result[1] == "sell" and INFO[0] == 'employee':
            print('Sell')
        elif result[0] == "store" and result[1] == "DBMgmt" and INFO[0] == 'employee':
            print('DB Management')
        elif result[0] == "store" and result[1] == "sell" and INFO[0] != 'employee':
            print('YOU MUST BE LOGGED IN AS AN EMPLOYEE TO ACCESS THIS FEATURE')
        elif result[0] == "store" and result[1] == "DBMgmt" and INFO[0] != 'employee':
            print('YOU MUST BE LOGGED IN AS AN EMPLOYEE TO ACCESS THIS FEATURE')
        elif result[0] == "online" and result[1] == "browse":
            dbFunctions.browse()
        elif result[0] == "online" and result[1] == "search":
            dbFunctions.search()
        elif result[0] == "online" and result[1] == "purchaseItems":
            dbFunctions.purchase()
        elif result[0] == "online" and result[1] == "purchaseHistory":
            dbFunctions.order_history()
        elif result[1] == "quit":
            quit_early = True


if __name__ == "__main__":
    main_loop()