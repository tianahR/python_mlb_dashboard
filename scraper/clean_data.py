import pandas as pd

def clean_csv(filename,new_name):
    try:
    
        # CLEAN table
        
        # Load the CSV
        df = pd.read_csv(filename)
        
        # Remove invalid or junk rows
        df = df[df['0'].astype(str).str.strip().str.lower() != 'statistic']

        # remove footer/junk rows
        df = df[~df['0'].str.contains("History", na=False)] 
        df = df[~df['0'].str.contains("Retirements", na=False)] 

        # Drop the 'Top 25' column
        df = df.drop(columns=['4'])

        # Rename columns
        df.columns = ['Year', 'Statistic', 'Player', 'Team', 'Value']

        # Convert 'Value' to numeric (int or float)
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        # Drop exact duplicates
        df = df.drop_duplicates()

        # Reset index
        df = df.reset_index(drop=True)

        # Save cleaned CSV
        df.to_csv(new_name, index=False)
    except Exception as e:
        print("No such file to clean",e)
        
        
def clean_standing_csv(filename,new_name):
    
    try:

        #Load lines manually
        with open(filename, encoding='utf-8') as f:
            raw_lines = f.readlines()

        # Process each line to ensure it has 7 columns
        cleaned_rows = []
        for line in raw_lines:
            cols = [c.strip() for c in line.strip().split(',')]
            if len(cols) < 7:
                cols += [None] * (7 - len(cols))  
            elif len(cols) > 7:
                cols = cols[:7]  
            cleaned_rows.append(cols)

        # Step 3: Convert to DataFrame, skipping the first row (original header)
        columns = ['Year', 'Division', 'Team', 'Wins', 'Losses', 'WinPct', 'GamesBehind']
        df = pd.DataFrame(cleaned_rows[1:], columns=columns)
   
        
        # Remove invalid or junk rows
               
        df = df[~df['Team'].str.contains("Team", na=False)] 

        # remove footer/junk rows
        df = df[~df['Team'].str.contains("Standings", na=False)] 
        df = df[~df['Division'].str.contains("Seasonal", na=False)] 
        
        
        # Convert Wins and Losses to numeric
        df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce')
        df['Losses'] = pd.to_numeric(df['Losses'], errors='coerce')
        
        df = df.drop(columns=['WinPct'])
        df = df.drop(columns=['GamesBehind'])
        
         
        # Drop exact duplicates
        df = df.drop_duplicates()

        # Reset index
        df = df.reset_index(drop=True)

        # Save cleaned CSV
        df.to_csv(new_name, index=False)
    except Exception as e:
        print("Failed",e)
        
        
def clean_team_csv(filename,new_name):
    try:
    
        # CLEAN table
        
        # Load the CSV
        df = pd.read_csv(filename)
        
        # Remove invalid or junk rows
        df = df[df['0'].astype(str).str.strip().str.lower() != 'statistic']

        # remove footer/junk rows
        df = df[~df['0'].str.contains("Review", na=False)] 
        df = df[~df['0'].str.contains("Seasonal", na=False)] 
        
        df = df[~df['1'].str.contains("To Be Determined", na=False)] 
       

        # Rename columns
        df.columns = ['Year', 'Statistic', 'Team', 'Value']

        # Convert 'Value' to numeric (int or float)
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        # Drop exact duplicates
        df = df.drop_duplicates()

        # Reset index
        df = df.reset_index(drop=True)

        # Save cleaned CSV
        df.to_csv(new_name, index=False)
    except Exception as e:
        print("No such file to clean",e)
    
clean_csv("data/table_1.csv","data/league_leader_hitting_stat.csv")
clean_csv("data/table_2.csv","data/league_leader_pitching_stat.csv")
clean_standing_csv("data/table_3.csv","data/team_standing_stat.csv")
# clean_team_csv("data/table_4.csv","data/team_leader_hitting_stat.csv")
# clean_team_csv("data/table_5.csv","data/team_leader_pitching_stat.csv")




