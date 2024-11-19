
userport= eval(input("Please enter the port number that you would like to use for the server"))
table_name = "table1"            
import mysql.connector
import pandas as pd 

def Connect_to_Mysql(userport):
    mydb = mysql.connector.connect(
        host="localhost",
        port=userport,
        user="root",
        passwd="root")
    return mydb

def Create_Table(file, mydb):
    if file.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.endswith('.txt'):
        df = pd.read_csv(file, delimiter="\t")
    else:
        raise ValueError("Only .csv, .txt, and .sql are allowed.")
    cursor = mydb.cursor
    columns = ""

    for i, colname in enumerate(df.columns):
        type_colname = type(df[colname].iloc[0])
    
        if i < len(df.columns) - 1: 
            if type_colname == int:
                columns += f"`{colname}` INT, "
            elif type_colname == float:
                columns += f"`{colname}` FLOAT, "
            elif type_colname == str:
                columns += f"`{colname}` VARCHAR(255), "
            else:
                columns += f"`{colname}` VARCHAR(255), "
        else: 
            if type_colname == int:
                columns += f"`{colname}` INT"
            elif type_colname == float:
                columns += f"`{colname}` FLOAT"
            elif type_colname == str:
                columns += f"`{colname}` VARCHAR(255)"
            else:
                columns += f"`{colname}` VARCHAR(255)"

    
    create_table_query = f"CREATE TABLE `{table_name}` ({columns});"

    cursor.execute(create_table_query)
    
    for i in range(len(df)):
        row = df.iloc[i] 
        placeholders = ""
        for i in range(len(row)):
            placeholders += "%s"
        if i < len(row) - 1:
            placeholders += ", "

    insert_query = f"INSERT INTO `{table_name}` VALUES ({placeholders});" 

    cursor.execute(insert_query, tuple(row))  # tuple converts the pandas series into a string
    
    
def filter_by_range(column_name, min_value, max_value):
    return f"SELECT * FROM `{table_name}` WHERE `{column_name}` BETWEEN {min_value} AND {max_value};"

def filter_by_character_pattern(column_name, pattern):
    return f"SELECT * FROM `{table_name}` WHERE `{column_name}` LIKE '%{pattern}%';"

def execute_query(mydb, query):
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()



    