# Lego Store Project
This app is used to manage a lego store. 

Employees can select the store mode option and which will require
the user to login to be able to access the options for store mode such as
   - Selling an item
   - Managing the inventory database
   - Managing the employees 
   
Users can select online mode which will only require a login/account creation for ordering items 
and checking purchase history. Online mode functions include
   - Browsing inventory
   - Searching for a specific item
   - Making a purchase
   - Checking purchase history

To get to store or online mode type in 'store' or 'online' and then you will be presented with options for that mode. When at the menus, in order to make a selection, enter the number of the option that contains the desired selection. 

To get out of the current mode, type 'main menu' from either mode and then type 'q' to quit the program. 

I used Python 3.8.4 on Mac OS to build this program. 
In order to run this program you will need the python modules listed below:
   - pyodbc (https://pypi.org/project/pyodbc/)
   - tabulate (https://pypi.org/project/tabulate/)
   - pyfiglet (https://pypi.org/project/pyfiglet/)
   - pytabby (https://pypi.org/project/pytabby/)

These can be installed by running the following commands:
   - pip3 install pyodbc
   - pip3 install tabulate
   - pip3 install pyfiglet
   - pip3 install pytabby

Once you have all these different modules installed, you can run the program by going into the menu folder within the lego-store-project file and running:
   'python3 app.py' 
in the terminal. 


TEST USER INFO
To run program with an admin account use the following information when asked to login:
   Employee ID: 1
   Password: 1234

To run program with a test user that has a test card saved to the account, use the following information:
   Email: TestCustomer
   Password: 1234

