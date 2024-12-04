import mysql.connector

# Conexión a MySQL


db_connection = mysql.connector.connect(
    host="matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
    user="MATCHIEAdmin",
    password="IeUniversity123",
    database ="LaLiga"
)

cursor = db_connection.cursor()

# Query a table
cursor.execute("SELECT * FROM DataDetail LIMIT 10;")
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
db_connection.close()
