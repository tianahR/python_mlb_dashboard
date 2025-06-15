
# import pandas as pd
# import sqlalchemy as sa
import sqlite3
import pandas as pd
import os

db_path = "../db/baseball_stat.db"

if os.path.exists(db_path):
    answer = input("The database exists.  Do you want to recreate it (y/n)?")
    if answer.lower() != 'y':
        exit(0)
    os.remove(db_path)
    
try:
    
    df = pd.read_csv("../scraper/data/league_leader_hitting_stat.csv")
    df1 = pd.read_csv("../scraper/data/league_leader_pitching_stat.csv")
    df2 = pd.read_csv("../scraper/data/team_standing_stat.csv")

    with sqlite3.connect("../db/baseball_stat.db",isolation_level='IMMEDIATE') as conn:    
        conn = sqlite3.connect("../db/baseball_stat.db",isolation_level='IMMEDIATE')
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS league_leader_hitting_stat")
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS league_leader_hitting_stat (
            league_hitting_id INTEGER PRIMARY KEY AUTOINCREMENT,          
            year INTEGER,
            statistic TEXT,
            player TEXT,
            team TEXT,
            value REAL
        )
        """)
        
        cursor.execute("DROP TABLE IF EXISTS league_leader_pitching_stat")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS league_leader_pitching_stat (
            league_pitching_id INTEGER PRIMARY KEY AUTOINCREMENT,          
            year INT,
            statistic TEXT,
            player TEXT,
            team TEXT,
            value REAL
        )
        """)
        
        cursor.execute("DROP TABLE IF EXISTS team_standing_stat")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_standing_stat (
            team_standing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INT,
            division TEXT,
            team TEXT,
            wins INT,
            loss INT
        )
        """)
        
        for _,row in df.iterrows():
            cursor.execute("""
            INSERT INTO league_leader_hitting_stat (year,statistic,player,team,value)
            VALUES (?,?,?,?,?)""", (row['Year'],row['Statistic'],row['Player'],row['Team'],row['Value']))
            
        for _,row in df1.iterrows():
            cursor.execute("""
            INSERT INTO league_leader_pitching_stat (year,statistic,player,team,value)
            VALUES (?,?,?,?,?)""", (row['Year'],row['Statistic'],row['Player'],row['Team'],row['Value']))
            
        for _,row in df2.iterrows():
            cursor.execute("""
            INSERT INTO team_standing_stat (year,division,team,wins,loss)
            VALUES (?,?,?,?,?)""", (row['Year'],row['Division'],row['Team'],row['Wins'],row['Losses']))
            
            
        conn.commit()
    print("Load data into baseball_stat.db")
    
    
except Exception as e:
    print(f'Error occured: {e}')
    
    
    
    
 

