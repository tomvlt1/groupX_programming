import mysql.connector
from datetime import datetime
from Globals import *
import csv
import pandas as pd
import random
import time


def openconnection():
    host="matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com"
    user="MATCHIEAdmin"
    password="IeUniversity123"
    database="LaLiga"

    db_config = {
        "host": host,
        "user": user,
        "password": password,
        "database":database 
    }
    db_connection = mysql.connector.connect(**db_config)
    return db_connection
    
def validate_user(username, password):
    db_connection = None  
    cursor = None
    try:
        db_connection = openconnection()
        cursor = db_connection.cursor()
        query = "SELECT UserName, IdUser FROM User WHERE LOWER(UserName) = LOWER(%s) AND Password = %s"
        cursor.execute(query, (username, password))
        queryresult = cursor.fetchone()
        if queryresult:
            setIDUser(int(queryresult[1]))  
            vmessage = "Login successful"
            vresult = True
            return vresult, vmessage, queryresult[0], queryresult[1]
        else:
            vmessage = "Incorrect credentials"
            vresult = False
            return vresult, vmessage, None, None
    except mysql.connector.Error as err:
        vmessage = f"Database Error: {err}"
        vresult = False
        return vresult, vmessage, None, None
    except Exception as e:
        vmessage = f"Error: {str(e)}"
        vresult = False
        return vresult, vmessage, None, None
    finally:
        cursor.close()
        db_connection.close()
            
def create_user(data):
    db_connection = None  
    cursor = None
    vcheck=0
    vmessage=''
    if not all(data):  
        vmessage="All fields must be filled" 
        vcheck=1
    if data[4]:
        try:
            shirt_number = int(data[4])  
        except ValueError:
            vmessage= vmessage + " Shirt Number must be an integer" 
            vcheck=1        
    try:
        date_string = data[5].strip()
        
        dob = datetime.strptime(date_string, '%Y-%m-%d').date()  
        
    except ValueError:
        vmessage = vmessage + " Date of Birth must be in the format yyyy-mm-dd"
        vcheck = 1
   
    if vcheck==0:
        try: 
            db_connection = openconnection()
            cursor = db_connection.cursor()
             
            check_query = "SELECT COUNT(*) FROM User WHERE LOWER(UserName) = LOWER(%s)"
            cursor.execute(check_query, (data[2],))  
            user_count = cursor.fetchone()[0]
            
            if user_count > 0:  
                vmessage = "Username already exists"
                vresult = False
            else:        
                query = """
                INSERT INTO User 
                (UserName, FirstName, LastName, Password, ShirtNumber,
                DateOfBirth, Gender, Nationality, FavoriteTeam) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    data[2],  
                    data[0],  
                    data[1],  
                    data[3],  
                    shirt_number,                 
                    dob,  
                    data[6],  
                    data[7],  
                    data[8]   
                )
                cursor.execute(query, values)
                db_connection.commit()
                vmessage = "User created successfully"
                vresult = True
        except:
            vmessage = "Error"
            vresult = False
        finally:
            cursor.close()
            db_connection.close()
        return vresult, vmessage
    
    else:
         return False, vmessage


def get_user_data(user_id):
    try:
              
        db_connection = openconnection()
        cursor = db_connection.cursor()

        query = """
        SELECT 
            FirstName, LastName, UserName, Password, ShirtNumber, DateOfBirth, Gender, Nationality, FavoriteTeam 
        FROM User 
        WHERE IdUser = %s
        """

        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        cursor.close()
        db_connection.close()
        
        return user_data 
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None  
    
def modify_user(user_id, data):
    db_connection = None 
    cursor = None
    vcheck=0
    vmessage=''
    if not all(data): 
        vmessage="All fields must be filled" 
        vcheck=1
    if data[4]:
        try:
            shirt_number = int(data[4])  
        except ValueError:
            vmessage= vmessage + " Shirt Number must be an integer" 
            vcheck=1        
    try:
        date_string = data[5].strip()
        
        dob = datetime.strptime(date_string, '%Y-%m-%d').date()  
        
    except ValueError:
        vmessage = vmessage + " Date of Birth must be in the format yyyy-mm-dd"
        vcheck = 1
   
    if vcheck==0:
        try:     
            db_connection = openconnection()
            cursor = db_connection.cursor()
            query = """
            UPDATE User
            SET UserName = %s, FirstName = %s, LastName = %s, Password = %s, ShirtNumber = %s, 
                DateOfBirth = %s, Gender = %s, 
                Nationality = %s, FavoriteTeam = %s
            WHERE IdUser = %s
            """

            cursor.execute(query, (
                data[2],    
                data[0],    
                data[1],    
                data[3],   
                data[4],              
                dob,    
                data[6],    
                data[7],    
                data[8],   
                user_id     
                ))
            db_connection.commit()

            cursor.close()
            db_connection.close()
            vresult=True
            vmessage= "User data updated successfully"
        except:
            vmessage = "Error"
            vresult = False
        finally:
            cursor.close()
            db_connection.close()
        return vresult, vmessage
    
    else:
         return False, vmessage
    
def delete_user(user_id):  
    try:  
        db_connection = openconnection()
        cursor = db_connection.cursor()
        
        query_files = """
        DELETE FROM LoadFiles
        WHERE idUser = %s
        """
        cursor.execute(query_files, (user_id,))
        db_connection.commit() 
        
        query_user_detail = """
        DELETE FROM DataDetail
        WHERE idUser = %s
        """
        cursor.execute(query_user_detail, (user_id,))
        db_connection.commit()  

        query_user = """
        DELETE FROM User
        WHERE IdUser = %s
        """
        cursor.execute(query_user, (user_id,))
        db_connection.commit() 

        cursor.close()
        db_connection.close()
        
        vresult = True
        vmessage = "User and related details deleted successfully"

    except Exception as e:
        vmessage = f"Error: {str(e)}"  
        vresult = False
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    return vresult, vmessage


    
def import_csv_to_database(file_path, user_id, load_id):
    db_connection = None  
    cursor = None
    print (file_path)
    print (user_id)
    print (load_id)
    try:
        db_connection = openconnection()
        cursor = db_connection.cursor()

        inserted_rows = 0  
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)

            header = next(csvreader)
            header = header[1:] 

            for row in csvreader:
               
                row = row[1:]
              
                try:
                    query = """
                        INSERT INTO DataDetail (
                            `Home Team`, `Away Team`, `Score`, `Half Time Score`,
                            `Match Excitement`, `Home Team Rating`, `Away Team Rating`,
                            `Home Team Possession %`, `Away Team Possession %`,
                            `Home Team Off Target Shots`, `Home Team On Target Shots`,
                            `Home Team Total Shots`, `Home Team Blocked Shots`,
                            `Home Team Corners`, `Home Team Throw Ins`,
                            `Home Team Pass Success %`, `Home Team Aerials Won`,
                            `Home Team Clearances`, `Home Team Fouls`,
                            `Home Team Yellow Cards`, `Home Team Second Yellow Cards`,
                            `Home Team Red Cards`, `Away Team Off Target Shots`,
                            `Away Team On Target Shots`, `Away Team Total Shots`,
                            `Away Team Blocked Shots`, `Away Team Corners`,
                            `Away Team Throw Ins`, `Away Team Pass Success %`,
                            `Away Team Aerials Won`, `Away Team Clearances`,
                            `Away Team Fouls`, `Away Team Yellow Cards`,
                            `Away Team Second Yellow Cards`, `Away Team Red Cards`,
                            `Home Team Goals Scored`, `Away Team Goals Scored`,
                            `Home Team Goals Conceeded`, `Away Team Goals Conceeded`,
                            `year`, `idLoad`, `idUser`
                        ) VALUES (
                            %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, %s,
                            %s, %s, 
                            %s, %s, 
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s, 
                            %s, %s,
                            %s, %s, 
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s, %s
                        )
                    """                
                    values = (
                        row[0], row[1], row[2], row[3],  
                        float(row[4]) if row[4] else 0.0,  
                        int(float(row[5])) if row[5] else 0,  
                        int(float(row[6])) if row[6] else 0,  
                        int(row[7]) if row[7] else 0,  
                        int(row[8]) if row[8] else 0,  
                        float(row[9]) if row[9] else 0.0,  
                        float(row[10]) if row[10] else 0.0,  
                        float(row[11]) if row[11] else 0.0,  
                        float(row[12]) if row[12] else 0.0,  
                        float(row[13]) if row[13] else 0.0,  
                        float(row[14]) if row[14] else 0.0,  
                        float(row[15]) if row[15] else 0.0,  
                        float(row[16]) if row[16] else 0.0,  
                        int(float(row[17])) if row[17] else 0,  
                        int(float(row[18])) if row[18] else 0,  
                        int(float(row[19])) if row[19] else 0,  
                        int(float(row[20])) if row[20] else 0,  
                        int(float(row[21])) if row[21] else 0,  
                        float(row[22]) if row[22] else 0.0,  
                        float(row[23]) if row[23] else 0.0,  
                        float(row[24]) if row[24] else 0.0,  
                        float(row[25]) if row[25] else 0.0,  
                        float(row[26]) if row[26] else 0.0,  
                        float(row[27]) if row[27] else 0.0,  
                        float(row[28]) if row[28] else 0.0,  
                        float(row[29]) if row[29] else 0.0,  
                        int(float(row[30])) if row[30] else 0, 
                        int(float(row[31])) if row[31] else 0,  
                        int(float(row[32])) if row[32] else 0,  
                        int(float(row[33])) if row[33] else 0,  
                        int(float(row[34])) if row[34] else 0, 
                        int(float(row[35])) if row[35] else 0,  
                        int(float(row[36])) if row[36] else 0,  
                        int(float(row[37])) if row[37] else 0,  
                        int(float(row[38])) if row[38] else 0,  
                        int(row[39]) if row[39] else 0,  
                        load_id, user_id  
                    )
                  
                    cursor.execute(query, values)
                   
                    inserted_rows += 1 
                except:
                    pass

        db_connection.commit()

        vmessage = f"{inserted_rows} rows were successfully inserted."
        return True, vmessage
    except:
        return False, "An error occurred while processing the file."
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    
def delete_last_insert_for_user(user_id):
        db_connection = None  
        cursor = None
        db_connection = openconnection()
        cursor = db_connection.cursor()
        try:
            query_get_last_idLoad = "SELECT MAX(idLoad) FROM DataDetail WHERE idUser = %s"
            cursor.execute(query_get_last_idLoad, (user_id,))
            last_idLoad = cursor.fetchone()[0]

            if last_idLoad is not None:
                query_delete_last = "DELETE FROM DataDetail WHERE idLoad = %s"
                cursor.execute(query_delete_last, (last_idLoad,))
                db_connection.commit()
                print(f"Registros con idLoad {last_idLoad} para el usuario {user_id} eliminados correctamente.")
            else:
                print(f"No se encontraron registros para el usuario {user_id}.")

        except Exception as e:
            print(f"Error eliminando registros para el usuario {user_id}: {e}")
            db_connection.rollback()
        finally:
            cursor.close()
            db_connection.close()
def check_csv_file(file_path):
    expected_headers = [
    "Home Team", "Away Team", "Score", "Half Time Score",
    "Match Excitement", "Home Team Rating", "Away Team Rating",
    "Home Team Possession %", "Away Team Possession %",
    "Home Team Off Target Shots", "Home Team On Target Shots",
    "Home Team Total Shots", "Home Team Blocked Shots",
    "Home Team Corners", "Home Team Throw Ins",
    "Home Team Pass Success %", "Home Team Aerials Won",
    "Home Team Clearances", "Home Team Fouls",
    "Home Team Yellow Cards", "Home Team Second Yellow Cards",
    "Home Team Red Cards", "Away Team Off Target Shots",
    "Away Team On Target Shots", "Away Team Total Shots",
    "Away Team Blocked Shots", "Away Team Corners",
    "Away Team Throw Ins", "Away Team Pass Success %",
    "Away Team Aerials Won", "Away Team Clearances",
    "Away Team Fouls", "Away Team Yellow Cards",
    "Away Team Second Yellow Cards", "Away Team Red Cards",
    "Home Team Goals Scored", "Away Team Goals Scored",
    "Home Team Goals Conceeded", "Away Team Goals Conceeded",
    "year"
]
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader, None)  
            header = header[1:]      
            if header is None:
                return False, "CSV file is empty."            
            if header != expected_headers:
                return False, f"CSV headers are incorrect."
    except FileNotFoundError:
        return False, "File does not exist."
    except IOError:
        return False, "Error opening the file."    
    if not file_path.lower().endswith('.csv'):
        return False, "The file is not a CSV file."
    return True, "File is valid."


def create_load_record(user_id, file_path):
    try:
        db_connection = openconnection()
        cursor = db_connection.cursor()

        query = "SELECT COALESCE(MAX(idLoadUser), 0) FROM LoadFiles WHERE idUser = %s"
        cursor.execute(query, (user_id,))
        last_load_id = cursor.fetchone()[0] or 0        
        new_load_id = last_load_id + 1
        insert_query = "INSERT INTO LoadFiles (idUser, idLoadUser, file_path,LoadDate) VALUES (%s, %s,%s, NOW())"
        cursor.execute("START TRANSACTION;") 
        cursor.execute(insert_query, (user_id, new_load_id,file_path))
        last_insert_id = cursor.lastrowid
        db_connection.commit()
        vmessage ="" 
        vresult=True
    except mysql.connector.Error as err:
        vmessage =f" {err}"
        vresult=False
        last_insert_id =0        
    cursor.close()
    db_connection.close()    
    return vresult, last_insert_id ,vmessage

def select_datadetail(year, iduser):
    idLoad=getDataset()
    if idLoad is not None:
          
        db_connection = None
        cursor = None
    
        try:       
            
            db_connection = openconnection()
            cursor = db_connection.cursor()
        
            query = "SELECT * FROM DataDetail WHERE year = %s AND idUser = %s AND `idLoad` = %s"
            cursor.execute(query, (int(year), int(iduser),int(idLoad),))
        
            results = cursor.fetchall()   
            column_names = [desc[0] for desc in cursor.description] 
        
            if results:        
                datos = pd.DataFrame(results, columns=column_names)
                return True, datos
            else: 
                return False, None
        except:     
            return False, None
        finally:       
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()

def select_datadetail_User():
    iduser1=getIDUser()
    idLoad1=getDataset()
    if iduser1 is not None and idLoad1 is not None:
        iduser=int(iduser1)
        idLoad=int(idLoad1)    

        db_connection = None
        cursor = None
    
        try:  
            db_connection = openconnection()
            cursor = db_connection.cursor()       
            
            query = "SELECT * FROM DataDetail WHERE `idUser` = %s AND `idLoad` = %s"
            cursor.execute(query, (iduser, idLoad,))
      
            records = cursor.fetchall()   
            
            column_names = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(records, columns=column_names)
            data=data.dropna()
          
            return data
        except:     
            return None
        finally:       
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
   
def fetch_years():
    iduser=getIDUser()
    idLoad=getDataset()
    if iduser is not None and idLoad is not None:
        iduser=int(iduser)
        idLoad=int( idLoad)
        try:
            db_connection = openconnection()
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT `year` FROM DataDetail WHERE `idUser` = %s AND `idLoad` = %s ORDER BY `year` ASC", (iduser, idLoad,))
            years = [row[0] for row in cursor.fetchall()]
            return years
        except :        
            return []
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
    else:
        return []

def fetch_teams_for_year(year):
    iduser=getIDUser()
    idLoad=getDataset()
    if iduser is not None and idLoad is not None:
        iduser=int(iduser)
        idLoad=int( idLoad)
   
        try:
            db_connection = openconnection()
            cursor = db_connection.cursor()
            cursor.execute("SELECT DISTINCT  dd.`Home Team`, COALESCE(ti.`icon`, '') AS `icon` FROM DataDetail dd LEFT JOIN TeamIcons ti ON dd.`Home Team` = ti.`Team` WHERE `year` = %s  AND dd.`idUser` = %s AND dd.`idLoad` = %s ORDER BY dd.`Home Team` ASC", (year,iduser,idLoad,))
            teams = [(row[0], row[1]) for row in cursor.fetchall()]
            return teams
        except:        
            return []
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
    else:
        return []
   
            
def GetRandomFacts(fact_qtt):
    iduser1=getIDUser()
    idLoad1=getDataset()
    if iduser1 is not None and idLoad1 is not None:
        iduser=int(iduser1)
        idLoad=int(idLoad1)    
    
        facts = []
        random.seed(time.time())  
        db_connection = None  
        cursor = None
        try:
            conn = openconnection()
            cursor = db_connection.cursor()        
            fact_queries = [
                {
                    "description": "fouls committed by Away Team",
                    "column": "`Away Team Fouls`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "fouls committed by Home Team",
                    "column": "`Home Team Fouls`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "highest excitement",
                    "column": "`Match Excitement`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "yellow cards for Home Team",
                    "column": "`Home Team Yellow Cards`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "yellow cards for Away Team",
                    "column": "`Away Team Yellow Cards`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "shots on target by Home Team",
                    "column": "`Home Team On Target Shots`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
                {
                    "description": "shots on target by Away Team",
                    "column": "`Away Team On Target Shots`",
                    "additional_info": "`Home Team`, `Away Team`",
                    "order": "DESC"
                },
            ]

            random.shuffle(fact_queries)

            for i in range(min(fact_qtt, len(fact_queries))):
                fact = fact_queries[i]
                try:
                    query = f"""
                        SELECT {fact['additional_info']}, {fact['column']}
                        FROM DataDetail WHERE `idUser` = %s AND `idLoad` = %s
                        ORDER BY {fact['column']} {fact['order']}
                        LIMIT 1;
                    """
                    cursor.execute(query, (iduser, idLoad,))
                    result = cursor.fetchone()
                    if result:
                        home_team, away_team, value = result
                        facts.append(f"{fact['description']}\n{home_team} - {away_team}\n{fact['column'].strip('`')}: {value}")
                        return facts
                except:        
                    return []
        except:        
            return []
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
    else:
        return None
            
  

def GetColumnNames(table_name):
    conn = None  
    cursor = None
    try:  
        
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`;")
        columns = [f"`{column[0]}`" for column in cursor.fetchall()]  
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        columns = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return columns

def filter_data_from_db(filters=None, columns=None,
                        order_by_column=None, order_by_direction=None,
                        unique_column=None):
    iduser1=getIDUser()
    idLoad1=getDataset()
   
    if iduser1 is not None and idLoad1 is not None:
        iduser=int(iduser1)
        idLoad=int(idLoad1)    
        conn = None
        cursor = None
        try:
            conn = openconnection()
            cursor = conn.cursor()

            if not columns or len(columns) == 0:
                column_str = "*"
            else:
                column_str = ", ".join(f"`{col}`" for col in columns)

            if unique_column:
                select_clause = f"DISTINCT `{unique_column}`"
                if column_str != "*":
                    select_clause += f", {column_str}"
            else:
                select_clause = column_str

            if select_clause.strip().startswith(","):
                select_clause = select_clause.lstrip(",")

            query = f"SELECT {select_clause} FROM `DataDetail` WHERE `idUser` = %s AND `idLoad` = %s"
            if filters:
                query +=  " AND "
                conditions = []
                for (col, op, val) in filters:
                    conditions.append(f"`{col}` {op} '{val}'")
                query +=" AND ".join(conditions)

            if order_by_column and order_by_direction:
                query += f" ORDER BY `{order_by_column}` {order_by_direction}"
            print(query)
            cursor.execute(query, (iduser, idLoad,))
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return pd.DataFrame(results, columns=column_names)
        except:
            print(f"Error")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return None


def get_headers():
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM `DataDetail`")
        headers = [row[0] for row in cursor.fetchall()]
        return headers[1:]  
    except Exception as e:
        print(f"Error fetching headers: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_column_datatype(column_name):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        query = f"SELECT `{column_name}` FROM `DataDetail` WHERE `{column_name}` IS NOT NULL LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            if isinstance(result[0], (int, float)):
                return "numerical"
            else:
                return "text"
    except Exception as e:
        print(f"Error determining datatype for column {column_name}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return "text"

def get_unique_values(column_name):
    iduser1=getIDUser()
    idLoad1=getDataset()
    if iduser1 is not None and idLoad1 is not None:
        iduser=int(iduser1)
        idLoad=int(idLoad1)    
        conn = None
        cursor = None
        try:
            conn = openconnection()
            cursor = conn.cursor()
            query = f"SELECT DISTINCT `{column_name}` FROM `DataDetail` WHERE `idUser` = %s AND `idLoad` = %s"
            cursor.execute(query, (iduser, idLoad,))
            results = cursor.fetchall()
            return [row[0] for row in results if row[0] is not None]
        except Exception as e:
            print(f"Error fetching unique values: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        return []


def get_operators_for_column(column_name):
    """
    Removed 'LIKE' operator as requested. Only basic operators remain.
    """
    datatype = get_column_datatype(column_name)
    if datatype == "numerical":
        return ["=", ">", "<", ">=", "<="]
    else:
        return ["="] 


def Select_Load_Files():
    iduser=int(getIDUser())
   
    try:
        db_connection = openconnection()
        cursor = db_connection.cursor()
        cursor.execute("SELECT idLoad,file_path,DATE_FORMAT(LoadDate, '%Y-%m-%d')  FROM LoadFiles WHERE `idUser` = %s ORDER BY idLoad DESC", (iduser,))
        vfiles= cursor.fetchall()
        return vfiles
    except :        
        return []
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close() 
            
            
            
