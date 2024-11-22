
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

def is_date_format(column):
    try:
        pd.to_datetime(column)
        return True  
    except (ValueError, TypeError):
        return False  

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
        
        if is_date_format(df[colname]) == True:
            type_colname = 'date'
        else:
            type_colname = type(df[colname].iloc[0])

            
        if i < len(df.columns) - 1: 
            if type_colname == int:
                columns += f"`{colname}` INT, "
            elif type_colname == float:
                columns += f"`{colname}` FLOAT, "
            elif type_colname == str:
                columns += f"`{colname}` VARCHAR(255), "
            elif type_colname == 'date':
                columns += f"`{colname}` DATE, "
            else:
                columns += f"`{colname}` VARCHAR(255), "
        else: 
            if type_colname == int:
                columns += f"`{colname}` INT"
            elif type_colname == float:
                columns += f"`{colname}` FLOAT"
            elif type_colname == str:
                columns += f"`{colname}` VARCHAR(255)"
            elif type_colname == 'date':
                columns += f"`{colname}` DATE"
            else:
                columns += f"`{colname}` VARCHAR(255)"

    
    create_table_query = f"CREATE TABLE `{table_name}` ({columns});"

    cursor.execute(create_table_query)
    
    for i in range(len(df)):
        row = df.iloc[i] 
        placeholders = ""
        for i in range(len(row)):
            placeholders += "%s"
        if i == len(row):
            placeholders += ", "

    insert_query = f"INSERT INTO `{table_name}` VALUES ({placeholders});" 

    cursor.execute(insert_query, tuple(row))  # tuple converts the pandas series into a string

def filter_by_range(mydb, column_name, min_value, max_value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` BETWEEN {min_value} AND {max_value};"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_exact_value(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` = '{value}';"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_not_equal(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` != '{value}';"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_null(mydb, column_name):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` IS NULL;"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_not_null(mydb, column_name):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` IS NOT NULL;"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_multiple_values(mydb, column_name, values_list):  #values have to be inpitted separated by a comma (",")
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` IN ({values_list});"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_not_in(mydb, column_name, values_list): #values have to be inpitted separated by a comma (",")
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` NOT IN ({values_list});"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_date_range(mydb, column_name, start_date, end_date):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` BETWEEN '{start_date}' AND '{end_date}';"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_greater_than(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` > {value};"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_less_than(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` < {value};"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_greater_than_or_equal(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` >= {value};"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_less_than_or_equal(mydb, column_name, value):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` <= {value};"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_starts_with(mydb, column_name, pattern):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` LIKE '{pattern}%';"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def filter_by_ends_with(mydb, column_name, pattern):
    query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` LIKE '%{pattern}';"
    cursor = mydb.cursor()
    cursor.execute(query)
    return cursor.fetchall()













    