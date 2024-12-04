import mysql.connector
import csv
from Globals import *
import os #to filename


# Database connection details
db_config = {
    "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
    "user": "MATCHIEAdmin",
    "password": "IeUniversity123",
    "database":"LaLiga"
}
# Function to validate user credentials
def validate_user(username, password):
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        # Query to check if the username and password exist
        query = "SELECT UserName,IdUser FROM User WHERE LOWER(UserName) = LOWER(%s) AND Password = %s"
        cursor.execute(query, (username, password))

        # Fetch result
        queryresult = cursor.fetchone()       
        if queryresult :
               
            # If a match is found
            setIDUser(int(queryresult[1])) #session
            vmessage = "Login successful"
            vresult=True
        else:
            # If no match is found
            vmessage = "Incorrect credentials"
            vresult=False
    except:
        vmessage = "Error"
        vresult=False
           
    cursor.close()
    db_connection.close()    
    return vresult, vmessage,queryresult[0],queryresult[1]
  
def create_user(name, password):
    try:
        # Conexión a la base de datos
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        # Query para insertar un nuevo usuario
        query = "INSERT INTO User (UserName, Password) VALUES (%s, %s)"
        values = (name, password)
        cursor.execute(query, values)  

        # Confirmar los cambios
        db_connection.commit()
         # If a match is found           
        vmessage = "Created"
        vresult=True
    except:
        vmessage = "Error"
        vresult=False
           
    cursor.close()
    db_connection.close()    
    return vresult, vmessage

# Función para registrar el archivo en la tabla LoadFiles
def create_load_record(user_id, file_path):
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        # Obtener el último idLoad para este usuario
        #COALESCE para que si no hay registros devuelva cero
        query = "SELECT COALESCE(MAX(idLoadUser), 0) FROM LoadFiles WHERE idUser = %s"
        cursor.execute(query, (user_id,))
        last_load_id = cursor.fetchone()[0] or 0
        # Obtener solo el nombre del archivo
        file_name = os.path.basename(file_path)
        # Crear un nuevo registro en LoadFiles
        new_load_id = last_load_id + 1
        insert_query = "INSERT INTO LoadFiles (idUser, idLoadUser, file_path,LoadDate) VALUES (%s, %s,%s, NOW())"
        # Start transaction
        cursor.execute("START TRANSACTION;") #para poder capturar el ultimo id creado
        cursor.execute(insert_query, (user_id, new_load_id,file_name))
         # Get the last inserted id (auto-incremented)
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

def import_csv_to_database(file_path, user_id, load_id):
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # # Saltar el encabezado (primera fila)
        header = next(csvreader)
        header = header[1:]  # Eliminar la primera columna del encabezado 

        for row in csvreader:
            # Eliminar la primera columna de cada fila
            row = row[1:]
            try:
                # Define la consulta SQL
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
                        %s, %s,%s
                    )
                """                
                values = (
                    row[0], row[1], row[2], row[3],  # `Home Team`, `Away Team`, `Score`, `Half Time Score`
                    float(row[4]) if row[4] else 0.0,  # `Match Excitement`, usa 0.0 si está vacío
                    int(float(row[5])) if row[5] else 0,  # `Home Team Rating`
                    int(float(row[6])) if row[6] else 0,  # `Away Team Rating`
                    int(row[7]) if row[7] else 0,  # `Home Team Possession %`
                    int(row[8]) if row[8] else 0,  # `Away Team Possession %`
                    float(row[9]) if row[9] else 0.0,  # `Home Team Off Target Shots`
                    float(row[10]) if row[10] else 0.0,  # `Home Team On Target Shots`
                    float(row[11]) if row[11] else 0.0,  # `Home Team Total Shots`
                    float(row[12]) if row[12] else 0.0,  # `Home Team Blocked Shots`
                    float(row[13]) if row[13] else 0.0,  # `Home Team Corners`
                    float(row[14]) if row[14] else 0.0,  # `Home Team Throw Ins`
                    float(row[15]) if row[15] else 0.0,  # `Home Team Pass Success %`
                    float(row[16]) if row[16] else 0.0,  # `Home Team Aerials Won`
                    int(float(row[17])) if row[17] else 0,  # `Home Team Clearances`
                    int(float(row[18])) if row[18] else 0,  # `Home Team Fouls`
                    int(float(row[19])) if row[19] else 0,  # `Home Team Yellow Cards`
                    int(float(row[20])) if row[20] else 0,  # `Home Team Second Yellow Cards`
                    int(float(row[21])) if row[21] else 0,  # `Home Team Red Cards`
                    float(row[22]) if row[22] else 0.0,  # `Away Team Off Target Shots`
                    float(row[23]) if row[23] else 0.0,  # `Away Team On Target Shots`
                    float(row[24]) if row[24] else 0.0,  # `Away Team Total Shots`
                    float(row[25]) if row[25] else 0.0,  # `Away Team Blocked Shots`
                    float(row[26]) if row[26] else 0.0,  # `Away Team Corners`
                    float(row[27]) if row[27] else 0.0,  # `Away Team Throw Ins`
                    float(row[28]) if row[28] else 0.0,  # `Away Team Pass Success %`
                    float(row[29]) if row[29] else 0.0,  # `Away Team Aerials Won`
                    int(float(row[30])) if row[30] else 0,  # `Away Team Clearances`
                    int(float(row[31])) if row[31] else 0,  # `Away Team Fouls`
                    int(float(row[32])) if row[32] else 0,  # `Away Team Yellow Cards`
                    int(float(row[33])) if row[33] else 0,  # `Away Team Second Yellow Cards`
                    int(float(row[34])) if row[34] else 0,  # `Away Team Red Cards`
                    int(float(row[35])) if row[35] else 0,  # `Home Team Goals Scored`
                    int(float(row[36])) if row[36] else 0,  # `Away Team Goals Scored`
                    int(float(row[37])) if row[37] else 0,  # `Home Team Goals Conceeded`
                    int(float(row[38])) if row[38] else 0,  # `Away Team Goals Conceeded`
                    int(row[39]) if row[39] else 0,  # `year`
                    load_id, user_id  # Valores adicionales
                )

                # Ejecutar la consulta
                cursor.execute(query, values)

            except Exception as e:
                print(f"Error inserting row: {row}")
                print(f"Error: {e}")

    # Confirmar transacciones
    db_connection.commit()

    # Cerrar conexiones
    cursor.close()
    db_connection.close()
    
def delete_last_insert_for_user(user_id):
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()

        try:
            # Obtén el MAX(idLoad) para el usuario específico
            query_get_last_idLoad = "SELECT MAX(idLoad) FROM DataDetail WHERE idUser = %s"
            cursor.execute(query_get_last_idLoad, (user_id,))
            last_idLoad = cursor.fetchone()[0]

            if last_idLoad is not None:
                # Elimina todos los registros con el idLoad correspondiente
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