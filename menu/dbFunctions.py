import pyodbc
cnx = pyodbc.connect(
    server="localhost",
    database="legoStore",
    user='sa',
    tds_version='7.4',
    password="Juan1997",
    port=1433,
    driver='/usr/local/lib/libtdsodbc.so'
)
cursor = cnx.cursor()
cursor.execute('SELECT * FROM legoStore.dbo.individual_lego_bricks')

for row in cursor:
    print(row)