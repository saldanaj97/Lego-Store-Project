from pytabby import Menu

# CONFIG dict to hold options for the menus
MAIN_MENU_CONFIG = {
    "case_sensitive": False,
    "screen_width": 80,
    "tabs": 
    [
        {
            "tab_header_input": "Main Menu",
            "items": 
            [
                {
                    "item_choice_displayed": "h",
                    "item_description": "Help",
                    "item_inputs": ["h"],
                    "item_returns": "help"
                },
                {
                    "item_choice_displayed": "q",
                    "item_description": "Quit Program",
                    "item_inputs": ["q"],
                    "item_returns": "quit"
                }
            ]
        }, 
        {
            "tab_header_input": "Store",
            "items": 
            [
                {
                    "item_choice_displayed": "1",
                    "item_description": "Sell",
                    "item_inputs": ["1"],
                    "item_returns": "sell"
                },
                {
                    "item_choice_displayed": "2",
                    "item_description": "Database Management",
                    "item_inputs": ["2"],
                    "item_returns": "DBMgmt"
                },
                {
                    "item_choice_displayed": "h",
                    "item_description": "Help",
                    "item_inputs": ["h"],
                    "item_returns": "help"
                },
                {
                    "item_choice_displayed": "q",
                    "item_description": "Quit Program",
                    "item_inputs": ["q"],
                    "item_returns": "quit"
                }
            ]   
        },
        {
            "tab_header_input": "Online",
            "items": 
            [
                {
                    "item_choice_displayed": "1",
                    "item_description": "Browse",
                    "item_inputs": ["1"],
                    "item_returns": "browse"
                },
                {
                    "item_choice_displayed": "2",
                    "item_description": "Search",
                    "item_inputs": ["2"],
                    "item_returns": "search"
                },
                {
                    "item_choice_displayed": "3",
                    "item_description": "Purchase Items",
                    "item_inputs": ["3"],
                    "item_returns": "purchaseItems"
                },
                ,
                {
                    "item_choice_displayed": "4",
                    "item_description": "View/Edit Cart",
                    "item_inputs": ["4"],
                    "item_returns": "cart"
                },
                {
                    "item_choice_displayed": "5",
                    "item_description": "View Purchase History",
                    "item_inputs": ["5"],
                    "item_returns": "purchaseHistory"
                },
                {
                    "item_choice_displayed": "h",
                    "item_description": "Help",
                    "item_inputs": ["h"],
                    "item_returns": "help"
                },
                {
                    "item_choice_displayed": "q",
                    "item_description": "Quit Program",
                    "item_inputs": ["q"],
                    "item_returns": "quit"
                }
            ]   
        }
    ]
}
