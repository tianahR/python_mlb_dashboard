import sqlite3
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import os

from dotenv import load_dotenv

load_dotenv()

# DB_PATH = os.getenv("DB_PATH", "/etc/secrets/baseball_stat.db")

# LOCAL_DB_PATH = "baseball_stat.db"
# LOCAL_DB_PATH="../db/baseball_stat.db"
# RENDER_DB_PATH = "/etc/secrets/baseball_stat.db"
LOCAL_DB_PATH=os.getenv("LOCAL_DB_PATH")
RENDER_DB_PATH =os.getenv("RENDER_DB_PATH")

DB_PATH = RENDER_DB_PATH if os.path.exists(RENDER_DB_PATH) else LOCAL_DB_PATH

# conn = sqlite3.connect(DB_PATH, check_same_thread=False)

# Connect to SQLite DB

def fetch_data(year):
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            
            hitting = pd.read_sql_query("""
            SELECT h.year, h.player, h.statistic, h.value, h.team, s.division, s.wins, s.loss 
            FROM league_leader_hitting_stat h 
            LEFT JOIN team_standing_stat s ON h.year = s.year AND h.team = s.team 
            WHERE h.year = ?
            ORDER BY h.value DESC """,conn, params=(year,))
            
            pitching = pd.read_sql_query("""
            SELECT 
            p.year,
            p.statistic,
            p.player,
            p.team,
            p.value,
            t.division,
            t.wins,
            t.loss
            FROM league_leader_pitching_stat p
            LEFT JOIN team_standing_stat t
            ON p.year = t.year AND p.team = t.team WHERE p.year =? ORDER BY p.value DESC""",conn, params=(year,))
            
            
            standings = pd.read_sql_query("SELECT * FROM team_standing_stat WHERE year = ?", conn, params=(year,))
            
            return hitting, pitching, standings
    except Exception as e:
        print(f'Error occured as {e}')
    conn.close()
    

# chart showing how each team's performance changes across years.
def fetch_standings_all_years():
    try:
        
        with sqlite3.connect(DB_PATH) as conn:
            all_standings = pd.read_sql_query("""
                SELECT team, year, wins, loss,
                    ROUND(CAST(wins AS FLOAT) / (wins + loss), 3) AS win_pct
                FROM team_standing_stat
                ORDER BY year ASC
            """, conn)
        return all_standings
    except Exception as e:
         print(f'Error occured as {e}')
    conn.close()
    
    
# Group Teams by Division with Tabs in Dash
def fetch_team_standing() :
    
    try:
    
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Tables found:", tables)
        
        all_team_standings = pd.read_sql_query("SELECT * FROM team_standing_stat", conn)
        return all_team_standings
    except Exception as e:
        print("Database error:", e)
        raise
    # try:
    #     with sqlite3.connect(DB_PATH) as conn:
        # all_team_standings = pd.read_sql_query("SELECT * FROM team_standing_stat", conn)
        # return all_team_standings
        
    # except Exception as e:
    #     print(f'Error occured as {e}')  
    
    




# Load available years
def get_years():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            sql_statement = "SELECT DISTINCT year FROM team_standing_stat ORDER BY year"
            years = pd.read_sql_query(sql_statement, conn)
            return years['year'].tolist()
    except Exception as e:
        print(f'Error occured as {e}')
    conn.close()
    
    
try:
    
    conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables found:", tables)
except Exception as e:
    print("Database error:", e)
    raise

all_team_standings = fetch_team_standing()
if all_team_standings is not None:
    divisions = all_team_standings['division'].unique()

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # deploy to render.com


app.title = "MLB Baseball Dashboard"

# App layout
app.layout = html.Div([
    html.H1("MLB Baseball Dashboard - American League 1975-2025",   style={'textAlign': 'center', 'marginBottom': '40px',}),

    
    html.Div([
        html.Label("Select Year:", className="label"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(y), 'value': y} for y in get_years()],
            value=get_years()[0],
             clearable=False,
        className="dropdown"
            )
        ], className="control"),

    html.Div([
        html.Label("Minimum Value Threshold:", className="label"),
        dcc.Slider(id='value-slider', min=0, max=100, step=5, value=0,
                   marks={i: str(i) for i in range(0, 101, 20)},
                tooltip={"placement": "bottom", "always_visible": True},
                className='slider'
            )
       ], className="control slider-control"),
    # ], className="control-row"),
    

    html.Div([
        dcc.Tabs(id="tabs", value = divisions[0],
            
            children=[
            dcc.Tab(label=division, value=division) for division in divisions
        ])
    ], className = 'dash-tab'),

    html.Div(id='graph-container', children=[
            
            dcc.Graph(id='hitting-leader-chart'),
            dcc.Graph(id='pitching-leader-chart'),
            dcc.Graph(id='win-pie-chart'),
            dcc.Graph(id='team-trend-line-chart'),
            dcc.Graph(id="division-chart"),
        ], style={'padding': '0 30px'})
    ]),


# Callbacks to update graph
@app.callback(
    Output('hitting-leader-chart', 'figure'),
    Output('pitching-leader-chart', 'figure'),
    Output('win-pie-chart', 'figure'),
    Output('team-trend-line-chart', 'figure'),
    Output("division-chart", "figure"),
    Input('year-dropdown', 'value'),
    Input('value-slider', 'value'),
    Input("tabs", 'value')
)

def update_charts(year, threshold,selected_division):
    hitting, pitching, standings = fetch_data(year)
    all_standings = fetch_standings_all_years()
    filtered_df = all_team_standings[all_team_standings['division'] == selected_division]
    

    hitting = hitting[hitting['value'] >= threshold]
    pitching = pitching[pitching['value'] >= threshold]

    fig_hit = px.bar(
        hitting,
        x="player", y="value", color="statistic",
        title=f"Hitting Leaders - {year}"
    )

    fig_pitch = px.bar(
        pitching,
        x="player", y="value", color="statistic",
        title=f"Pitching Leaders - {year}"
    )

    fig_pie = px.pie(
        standings,
        values='wins',
        names='division',
        title=f"Win Distribution by Division - {year}"
    )


    
    # New line chart of team performance over time
    # Use hover_data to see team/year details
    fig_line = px.line(
        all_standings,
        x="year", y="win_pct", color="team",
        title="Team Win Percentage Over Time",
        markers=True
    )
    
    # Group teams by division using tabs 
    fig_div = px.line(
        filtered_df,
        x="year",
        y="wins",
        color="team",
        markers=True,
        title=f"Team Wins Over Time - {selected_division} Division"
    )
    
    fig_div.update_layout(transition_duration=300)

    return fig_hit, fig_pitch, fig_pie,fig_line,fig_div
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 
