import sqlite3

def get_connection():
    try:
        return sqlite3.connect("../db/baseball_stat.db")
    except sqlite3.Error as e:
        print(f"Error Connecting to DB :{e}")
        return None


def show_menu():
    print("\n Choose a query:")
    print("1: View the first 10 records")
    print("2: Get Distinct statistics")
    print("3: Filter by year ([1975 - 2026]")
    print("4: Find the top player for a specific stat (e.g., Home Runs) in 1975")
    print("5. Count how many stats each player led")
    print("6: Show the team with most wins in each year")
    print("7: Calculate win percentage and list all teams with more than 60% win rate")
    print("8: Group average pitching stat values by year for a specific stat")
    print("9: Analyze how pitching leaders relate to team performance")
    print("10:List hitting leaders along with their team standings")
    
    print("11: Exit")
    
    
def first_10_records_h(conn):
    try:
        cursor = conn.execute("SELECT * FROM league_leader_hitting_stat LIMIT 10")
        results = cursor.fetchall()
        if results:
            print("First 10 records")
        for row in results:
                print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
def distinct_statistic_h(conn):
    try:
        cursor = conn.execute("SELECT DISTINCT statistic FROM league_leader_hitting_stat")
        results = cursor.fetchall()
        if results:
            print("Distinct statistics")
            # print(results)
            for row in results:
                print(f"{row} ")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        

def filter_by_year_h(conn):
    try:
        year = input("Enter year between [1975 - 2026]").strip()
        cursor = conn.execute("SELECT statistic, player, team, value FROM league_leader_hitting_stat WHERE year =?", (year,))
        results = cursor.fetchall()
        if results:
            print("Filter by year")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        


    
def top_player_specific_stat(conn):
    try:
        year = input("Enter year between [1975 - 2026]").strip()
        stat = input("Enter Statistic eg : Home Runs").strip()
        cursor = conn.execute("""
        SELECT statistic, player, team, value FROM league_leader_hitting_stat 
        WHERE year =? AND statistic = ? ORDER BY value DESC LIMIT 1""", (year,stat))
        
        results = cursor.fetchall()
        if results:
            print(f"Top Player in {stat} in year {year}")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
        
def stat_led_by_player_count(conn):
    try:
        
        cursor = conn.execute("""SELECT player, COUNT(*) AS stat_titles
        FROM league_leader_hitting_stat
        GROUP BY player
        ORDER BY stat_titles DESC""")
        
        results = cursor.fetchall()
        if results:
            print("How many stats each player led")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
        
def team_with_most_wins(conn):
    try:
        
        cursor = conn.execute("""SELECT year, team, MAX(wins) AS max_wins
        FROM team_standing_stat
        GROUP BY year;""")
        
        results = cursor.fetchall()
        if results:
            print("Team with Most Wins")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
def team_with_60percent_win_rate(conn):
    try:
        
        cursor = conn.execute("""SELECT team, year, wins, loss,
       ROUND(CAST(wins AS REAL) / (wins + loss), 3) AS win_pct
        FROM team_standing_stat
        WHERE (wins + loss) > 0
        AND (CAST(wins AS REAL) / (wins + loss)) > 0.6
        ORDER BY win_pct DESC;""")
        
        results = cursor.fetchall()
        if results:
            print("Team with 60 % win rate")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
def group_average_pitching_stat(conn):
    try:
        
        stat = input("Enter Statistic eg : Home Runs").strip()
        cursor = conn.execute("""
        SELECT year, ROUND(AVG(value), 2) AS avg_value  
        FROM league_leader_pitching_stat WHERE statistic = ? GROUP BY year ORDER BY year;""", (stat,))
        
        results = cursor.fetchall()
        if results:
            print(f"Group average pitching stat values by year for {stat}")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
        
def relation_pitching_leaders_team_performance(conn):
    try:
        
        
        cursor = conn.execute("""
        SELECT p.year, p.player, p.statistic, p.value, s.team, s.wins, s.loss 
        FROM league_leader_pitching_stat p JOIN team_standing_stat s ON p.year = s.year 
        AND p.team = s.team WHERE p.statistic = 'Wins' ORDER BY p.value DESC;""")
        results = cursor.fetchall()
        if results:
            print("Pitching leaders relate to team performance")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
        
def hitting_leaders(conn):
    
    try:
        
        
        cursor = conn.execute("""
        SELECT h.year, h.player, h.statistic, h.value, s.division, s.wins, s.loss
        FROM league_leader_hitting_stat h
        JOIN team_standing_stat s ON h.year = s.year AND h.team = s.team
        WHERE h.statistic = 'Batting Average'
        ORDER BY h.value DESC;""")
        
        results = cursor.fetchall()
        if results:
            print("List hitting leaders along with their team standings")
            # print(results)
            for row in results:
                print(f"{row} \n")
        else:
            print("No records found")
    except Exception as e:
        print(f"Error occured, {e}")
        
        
    
    
    
        
    
        
        
def main():
    conn = get_connection()
    if not conn:
        return
    
    try:
        while True:
            show_menu()
            
            choice = input("What query to execute?: ").strip()
            if choice == "1":
                first_10_records_h(conn)
            elif choice == "2":
                distinct_statistic_h(conn)
            elif choice == "3":
                filter_by_year_h(conn)
            elif choice == "4":
                top_player_specific_stat(conn)
            elif choice == "5":
                stat_led_by_player_count(conn)
            elif choice == "6":
                team_with_most_wins(conn)
            elif choice == "7":
                team_with_60percent_win_rate(conn)
            elif choice == "8":
                group_average_pitching_stat(conn)
            elif choice == "9":
                relation_pitching_leaders_team_performance(conn)
            elif choice == "10":
                hitting_leaders(conn)
                
            
                
            elif choice == "11":
                print("See you next time")
                break
            else:
                print("Not a valid choice")
    finally:
        conn.close()
        
if __name__ == "__main__":
    main()