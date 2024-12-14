import mysql.connector 
import pandas as pd
from config import (host,user,password,database)

db_config = {
    "host": host,
    "user": user,
    "password": password,
    "database": database
}


try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM DataDetail;"
    cursor.execute(query)
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(records, columns=column_names)
except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
