# PYTHON_MLB_DASHBOARD - Web Scraping and Dashboard Project

## ABOUT THE PROJECT

A Python program that retrieves data from BASEBALL ALMANAC website : https://www.baseball-almanac.com/yearmenu.shtml and display the results in an interactive dashboard.
The website contains the History of Major League Baseball in a Yearly Format.

<p>There are 289 pages to scrape. Among them, we have :
    The History of the American League From 1901 to 2025,
    The History of the National League From 1876 to 2025,
    The History of the Federal League From 1914 to 1915,
    The History of the Players League From 1890 - 1890,
    The History of the Union Association From 1884 - 1884,
    The History of the American Association From 1882 - 1891
</p>
<p>On EACH page, there are :
    League Leader in Hitting Statistics (Top 25),
    League Leader in Pitching Statistics (Top 25),
    Final Standings for every Team,
    Links to every Team Roster,
    Team Leader for Hitting & Pitching Stats,
    Retirements / Final Season Played Lists,
    Rookies / First Season Played Lists,
    Links to Seasonal Events
</p>

<b>For this project</b> - I retrieve data from the history of the American League from <b>1975 to 2025</b>

The project is divided into :

- ### Web Scraping program :

    <p>To scrape data from the website, I use <b>Selenium</b>. and saved the raw data into CSV format for each dataset :
        League Leader in Hitting Statistics (Top 25),
        League Leader in Pitching Statistics (Top 25),
        Final Standings for every Team,
        Team Leader for Hitting Stats,
        Team Leader for Pitching Stats</p>
    <p>For the analysis and data visualization, I use 3 datasets : League Leader in Hitting Statistics (Top 25), League Leader in Pitching Statistics (Top 25), Final Standings for every Team</p>

- ### Database import program :

    <p>Import the CSV files into a <b>SQLite database </b>.</p>
    <p>Before storing the data in a SQLite database, with each CSV file as a separate table, I clean and transform the raw data into a structured format.</p>

- ### Database query program :
  Query the database via command line.
- ### Dashboard program :
  Build an interactive dashboard using <b>Dash</b> to display the insights.

## TECH STACK USED :

  <p>Python, SQLITE, Selenium, Numpy, Pandas, Matplotlib, Plotly, Seaborn, Dash</p>

## STEPS TO RUN THE PROGRAM :

- Clone the program
- Create the virtual environment
    <p>Windows users enter the following commands:
    python -m venv .venv
    source .venv/Scripts/activate
    code .

  Mac and Linux users enter the following commands:
  python3 -m venv .venv
  source .venv/bin/activate
  code .</p>

  Once your virtual environment is activated, you see .venv as part of your terminal prompt.

  Important: Open the VSCode command pallette (ctrl-shift P). In the `Python: Select Interpreter` option, choose the one with `.venv`. You can use the search box at the top to find it. If you have any terminal sessions open, close them, and open a new one. You will see `(.venv)` in your terminal prompt.

- From the VSCode terminal session, enter the command:

```shell
pip install -r requirements.txt
```

<p>
Once this is done, you can run the project :

- cd to scraper folder and run scraper.py
- After run clean_data.py
- To import the csv to the database : cd to database folder and run import_to_sqlite.py
- To query the database via command line, cd to cli folder and run query_mlb.py
- To build the interactive Dashboard - cd to dashboard folder and run app.py
  Dash is running on http://127.0.0.1:8050/

</p>

## Some screenshots of images in the Dashboard

![newplot](https://github.com/user-attachments/assets/f0bcaa2f-afc2-4b9a-b1a3-891fe94b9d0e)![newplot (1)](https://github.com/user-attachments/assets/b36e04ec-732d-498c-8dfe-71304ffef37c)
![newplot (2)](https://github.com/user-attachments/assets/c73e758f-7392-4667-a83d-3114ca6ca5b0)
![newplot (3)](https://github.com/user-attachments/assets/477a11c1-8d6b-4ec7-925e-11336239891d)
![newplot (4)](https://github.com/user-attachments/assets/265cc603-1879-42e4-806e-2d2a839ceb41)


