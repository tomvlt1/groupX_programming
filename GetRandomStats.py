import mysql.connector
import random
import time



def GetRandomFacts(fact_qtt):
    db_config = {
    "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
    "user": "MATCHIEAdmin",
    "password": "IeUniversity123",
    "database": "LaLiga"}
    facts = []
    random.seed(time.time())  
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

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
                FROM DataDetail
                ORDER BY {fact['column']} {fact['order']}
                LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                home_team, away_team, value = result
                facts.append(f"{fact['description']}\n{home_team} - {away_team}\n{fact['column'].strip('`')}: {value}")
        except mysql.connector.Error as err:
            facts.append(f"Error retrieving fact: {fact['description']}")

    cursor.close()
    conn.close()
    return facts

def GetColumnNames(table_name):
    db_config = {
    "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
    "user": "MATCHIEAdmin",
    "password": "IeUniversity123",
    "database": "LaLiga"}
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`;")
        columns = [f"`{col[0]}`" for col in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        columns = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return columns

if __name__ == "__main__":
    print(GetRandomFacts(5))
    print(GetColumnNames("DataDetail"))
    print("hello world \n hello")
