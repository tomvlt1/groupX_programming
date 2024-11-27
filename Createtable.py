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
    
    mydb.commit()
    cursor.close()
    
    
    
    