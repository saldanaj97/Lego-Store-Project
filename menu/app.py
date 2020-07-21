from pytabby import Menu
import pyfiglet
import modes
import menu_configs
import subprocess

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

        "In order to make a selection, enter the number of the option that contains the desired selection. \n"
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
        if result[1] == "storeMode":
            print("Store Mode")
        elif result[1] == "onlineMode":
            print("Online mode")
        elif result[1] == "help":
            print_help()
        elif result[1] == "quit":
            quit_early = True


if __name__ == "__main__":
    main_loop()