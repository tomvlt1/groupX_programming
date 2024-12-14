import mysql.connector
import random
import time

# Database configuration
db_config = {
    "host": "matchie.clkcos8e6w49.eu-north-1.rds.amazonaws.com",
    "user": "MATCHIEAdmin",
    "password": "IeUniversity123",
    "database": "LaLiga"
}

def GetRandomFacts(fact_qtt):
    facts = []
    random.seed(time.time())  # Changes the seed every time the program is called
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Predefined list of meaningful columns for match-level facts
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

    # Shuffle the queries to introduce randomness
    random.shuffle(fact_queries)

    for i in range(min(fact_qtt, len(fact_queries))):
        fact = fact_queries[i]
        try:
            # Query for the specific fact
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
    #for debugging
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Query to fetch column names
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`;")
        columns = [f"`{column[0]}`" for column in cursor.fetchall()]  # Properly escape column names
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
    print(GetRandomFacts(5))  # Example output: ['Team with most Goals: Real Madrid, 100', 'Random Team: Barcelona', 'Team with most Yellow Cards: Real Betis, 50']
    #print(GetColumnNames("DataDetail"))  # Example output: ['`Team`', '`Goals`', '`Yellow Cards`', '`Red Cards`', '`Fouls`', '`Corners`', '`Shots`', '`Shots on Target`', '`Possession`', '`Passes`', '`Pass Accuracy`', '`Distance Covered (Kms)`', '`Cleansheets`', '`Goals Conceded`', '`Saves`', '`Passes Completed`', '`Last
    
    print("hello world \n hello")