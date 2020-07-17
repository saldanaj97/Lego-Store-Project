#!/usr/bin/env python3
from consolemenu import *
from consolemenu.items import *
from consolemenu.screen import *

# Store mode menu
def store_mode (): 
    # Title and directions
    store_mode_menu = ConsoleMenu("Juan\'s Lego Store", "Store Mode", 
    formatter=MenuFormatBuilder()
    .set_title_align('center')
    .set_subtitle_align('center'))

    # List the different store mode operations in the menu
    store_operations = ["Sell", "Order Management", "Database Management", "Delivery Management"]
    operation = SelectionMenu.get_selection(store_operations)

    # Show the store mode menu
    store_mode_menu.show()

# Online mode menu
def online_mode(): 
    # Title and directions
    online_mode_menu = ConsoleMenu("Juan\'s Lego Store", "Online Mode", 
    formatter=MenuFormatBuilder()
    .set_title_align('center')
    .set_subtitle_align('center'))
    
    # List the different store mode operations in the menu
    online_operations = ["Browse", "Search", "View Purchase History"]
    operation = SelectionMenu.get_selection(online_operations)

    # Show the store mode menu
    online_mode_menu.show()

def main_menu ():
    # Make the menu with a formatted title and description 
    menu = ConsoleMenu("Juan\'s Lego Store", "Main Menu", prologue_text="Select an operating \
mode by typing the number and pressing enter. Go into store mode if you are an employee. Otherwise, go into \
online mode to make purchases.", formatter=MenuFormatBuilder()
                                .set_title_align('center')
                                .set_subtitle_align('center'))

    # A FunctionItem runs a Python function when selected
    store_mode_function = FunctionItem("Store Mode", store_mode)
    online_mode_function = FunctionItem("Online Mode", online_mode)

    # Once we're done creating them, we just add the items to the menu
    menu.append_item(store_mode_function)
    menu.append_item(online_mode_function)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()

# Main Function 
def main():
    main_menu()

# Run Main 
main()