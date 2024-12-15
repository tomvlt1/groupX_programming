import mysql.connector
from config import *


# Conexión a MySQL
db_host = host
db_user = user
db_password = password
db_name = database

# Database connection details
db_config = {
    "host": db_host,
    "user": db_user,
    "password": db_password,
    "database":db_name 
}
try:
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()

    # LaLiga
    cursor.execute("CREATE DATABASE IF NOT EXISTS LaLiga;")
    cursor.execute("USE LaLiga;")  

    # User
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Password VARCHAR(255),
    ShirtNumber INT,    
    DateOfBirth DATE,
    Gender VARCHAR(50),
    Nationality VARCHAR(255),
    FavoriteTeam VARCHAR(255)
    )  ;
        """)


    #  Load
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LoadFiles (
        idLoad INT AUTO_INCREMENT PRIMARY KEY,
        idLoadUser INT,
        idUser INT,   
        file_path  VARCHAR(255),  
        LoadDate DATE,
        FOREIGN KEY (idUser) REFERENCES User(idUser)
    );
    """)

    # DataDetail
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DataDetail (
        `idDataDetail` INT AUTO_INCREMENT PRIMARY KEY,    
        `Home Team` VARCHAR(255),
        `Away Team` VARCHAR(255),
        `Score` VARCHAR(5),
        `Half Time Score` VARCHAR(5),
        `Match Excitement` FLOAT,
        `Home Team Rating` FLOAT,
        `Away Team Rating` FLOAT,
        `Home Team Possession %` INT,
        `Away Team Possession %` INT,
        `Home Team Off Target Shots` FLOAT,
        `Home Team On Target Shots` FLOAT,
        `Home Team Total Shots` FLOAT,
        `Home Team Blocked Shots` FLOAT,
        `Home Team Corners` FLOAT,
        `Home Team Throw Ins` FLOAT,
        `Home Team Pass Success %` FLOAT,
        `Home Team Aerials Won` FLOAT,
        `Home Team Clearances` FLOAT,
        `Home Team Fouls` FLOAT,
        `Home Team Yellow Cards` FLOAT,
        `Home Team Second Yellow Cards` FLOAT,
        `Home Team Red Cards` FLOAT,
        `Away Team Off Target Shots` FLOAT,
        `Away Team On Target Shots` FLOAT,
        `Away Team Total Shots` FLOAT,
        `Away Team Blocked Shots` FLOAT,
        `Away Team Corners` FLOAT,
        `Away Team Throw Ins` FLOAT,
        `Away Team Pass Success %` FLOAT,
        `Away Team Aerials Won` FLOAT,
        `Away Team Clearances` FLOAT,
        `Away Team Fouls` FLOAT,
        `Away Team Yellow Cards` FLOAT,
        `Away Team Second Yellow Cards` FLOAT,
        `Away Team Red Cards` FLOAT,
        `Home Team Goals Scored` INT,
        `Away Team Goals Scored` INT,
        `Home Team Goals Conceeded` INT,
        `Away Team Goals Conceeded` INT,
        `year` INT,
        `idLoad` INT,
        `idUser` INT,         
        FOREIGN KEY (idUser) REFERENCES User(idUser),
        FOREIGN KEY (idLoad) REFERENCES LoadFiles(idLoad)
    );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  `TeamIcons` (
                    `Team`  VARCHAR(255),
                    `Icon`  VARCHAR(255)
                    ) ;
        """)

    
    db_connection.commit()
    print("OK")

    cursor.close()
    db_connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()

