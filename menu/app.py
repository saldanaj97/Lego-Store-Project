from pytabby import Menu
import menu_configs
import modes
import pyfiglet
import dbFunctions

def print_help():
    help_text = (
        "This app is used to manage a lego store.\n\nEmployees can select the store mode option and which will require "
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
        "To get out of the current mode, type 'main menu' from either mode and then type 'q' to quit the program. \n"

    )
    print(help_text)


def main_loop(): 
    # Logic for the app
    menu = Menu(menu_configs.MAIN_MENU_CONFIG)
    store_name = pyfiglet.figlet_format("The Lego Store")
    quit_early = False
    while not quit_early:
        print(store_name)
        result = menu.run(message={"store": "You are now in store mode.", "online": "You are now in online mode."})
        #print(result)
        if result[1] == "help":
            print_help()
        elif result[0] == "online" and result[1] == "browse":
            dbFunctions.browse()
        elif result[1] == "quit":
            quit_early = True


if __name__ == "__main__":
    main_loop()