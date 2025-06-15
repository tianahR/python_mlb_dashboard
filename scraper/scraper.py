import os
# import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from io import StringIO
import re


BASE_URL = "https://www.baseball-almanac.com/yearmenu.shtml"

DATA_DIR = "data"

# Set user-agent to mimic a browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/125.0.0.0 Safari/537.36"




# Setup driver 
def setup_driver():
    options = Options()   
    options.add_argument("--headless")
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    return driver


# extract all year url in the base url
def scrape_year_links(driver):
    """Get all year links from main menu page."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    year_links = []
    year_elements =  wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".datacolBox a")))

    for el in year_elements:
        text = el.text.strip()
        href = el.get_attribute("href")
        
        # League_Type
        
        match = re.search(r'yr\d+([a-z])\.shtml', href)
        result = match.group(1) if match else ""
        
        if result == 'a':
            league_type = 'American League'
        elif result =='n':
            league_type= 'National League'
        elif result == 'f':
            league_type = 'Federal League'
        elif result == 'p':
            league_type == 'Players League'
        elif result == 'u':
            league_type = 'Union Association'
        
        
        match = re.search(r'yr(\d{4}[a-z])\.shtml', href)
        result = match.group(1) if match else ""
        if result in ['1882a','1883a','1884a','1885a','1886a','1887a','1888a','1889a','1890a','1891a']:
            league_type = 'American Association'

        if text.isdigit() and "yearly" in href:
            year_links.append((text, href,league_type))
    return year_links



def scrape_table(url,year):
    
    driver = setup_driver()
   
    try:  
        driver.get(url)  

        # Tell Selenium how long to wait for the whole page to load
        driver.set_page_load_timeout(60) 

        # Find all data tables (they have class 'boxed')
        tables = driver.find_elements(By.XPATH, "//div[@class='ba-table']//table[@class='boxed']")

        # Extract tables into DataFrames
        dataframes = []
        for table in tables:
            html = StringIO(table.get_attribute('outerHTML'))
            df = pd.read_html(html)[0]
            df.insert(0, "Year", year)
            dataframes.append(df)
            
        return dataframes

        
    except Exception as e:
        print("Failed 1",e)
        return None
            
    finally:
        driver.quit()
        
        
def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    driver = setup_driver()

    try:
        year_links = scrape_year_links(driver)
        print(f"Found {len(year_links)} years to scrape")
        
        # load year_links to CSV file 
        df = pd.DataFrame(year_links)
        df.columns = ['Year','URL','Type of League']
        df.to_csv(os.path.join(DATA_DIR, "year_links.csv"), index=False)  
        
        # Loop through a range of year to scrape each year's data for American league only
        
        for year in range(1975, 2026):  
            print(f"Processing year {year}")
            url = f"https://www.baseball-almanac.com/yearly/yr{year}a.shtml"
            driver.get(url)
           
            driver.set_page_load_timeout(60) # Tell Selenium how long to wait for the whole page to load
            
            
            dataframes = scrape_table(url,year)
            
            # Save each table to CSV
            for idx, df in enumerate(dataframes):
                # Check if the file exists
                filename = os.path.join(DATA_DIR,f'table_{idx+1}.csv')
                
                if os.path.exists(filename):
                    # Append data without writing the header again
                    df[2:].to_csv(filename, mode='a', header=False, index=False)
                    
                else:
                    # File doesn't exist, write with header
                    df[2:].to_csv(filename, mode='w', header=True, index=False)
            
        
        
    except Exception as e :
        print("Failed 2",e)
                    
                               
    finally:
        driver.quit()
        
        
    
    
        
        
        

if __name__ == "__main__":
    main()
