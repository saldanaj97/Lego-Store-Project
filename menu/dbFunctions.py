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

def browse():
    # Query the database
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM legoStore.dbo.individual_lego_bricks')
    
    # Put the data from the query into a list
    query_result = cursor.fetchall()
    block_inventory = [list(i) for i in query_result]

    # Print the data for individual blocks
    headers = ["Item ID", "Size", "Color", "Price($)", "In stock", "Type"]
    print("\n\nIndividual Piece Inventory")
    print(tabulate(block_inventory,headers, floatfmt=".2f"))

    # Query the database for the block set data
    cursor.execute('SELECT * FROM legoStore.dbo.lego_brick_sets')
    query_result = cursor.fetchall()
    set_inventory = [list(i) for i in query_result]

    # Print the data for the sets
    headers = ["Set ID", "Name", "Piece Count", "In stock"]
    print("\n\nSet Inventory")
    print(tabulate(set_inventory,headers))
    print("\n\n")
    
