import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

def initialize_webdriver():
    """Initialize and return a Selenium WebDriver with common Chrome options."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')  # Enable headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Initialize and return the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver


def league_table():
    """
This function scrapes the Premier League table from the BBC Sport website. 
It retrieves the HTML content of the page, parses it using BeautifulSoup,
and extracts the relevant data to create a DataFrame. 
"""
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    headers = []

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table')

        # Extract column headers
        for i in table.find_all('th'):
            title = i.text
            headers.append(title)
        
        league_table = pd.DataFrame(columns = headers)

        # Extract row data and populate the DataFrame
        for j in table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            # Extract text from each cell in the row and create a list
            row = [i.text for i in row_data]
            # get the current length of the DataFrame to determine the next index for insertion
            length = len(league_table)
            # Add the row to the DataFrame at the next available index
            league_table.loc[length] = row

        # Split the 'Team' column to extract 'Position' and 'Team' information
        league_table[['Position', 'Team']] = league_table['Team'].str.extract(r'(\d+)([A-Za-z]+)')
        # Move 'Position' column from last to the front
        league_table.insert(0, 'Position', league_table.pop('Position'))
        #Drop unnecessary column
        league_table.drop(['Form, Last 6 games, Oldest first'], axis=1, inplace=True)
    except AttributeError: 
        print("Could not find the table element on the page. Please check the website structure.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the HTTP request: {e}")
    except TimeoutError:
        print("The request timed out. Please check your internet connection or try again later.")  



    return league_table


def top_scorers():
    """
    This function scrapes the top scorers
    of the Premier League from the BBC Sport website.
    """
    url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
    headers = []
    try:

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table')

        for i in table.find_all('th'):
            title = i.text
            headers.append(title)
        
        top_scorers = pd.DataFrame(columns = headers)

        for j in table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(top_scorers)
            top_scorers.loc[length] = row

        # The 'Name' column contains both the player's name and club information. 
        top_scorers.Name = top_scorers.Name.replace(r'([A-Z])', r' \1', regex=True).str.split()
        # Remove duplicate words from the 'Name' column while preserving the order of words
        # the lambda function uses a dictionary to remove duplicates while preserving the order of words in the 'Name' column. 
        # It converts the list of words into a dictionary (which inherently removes duplicates) and then back into a list, 
        # which is then joined back into a string.
        top_scorers.Name = top_scorers.Name.apply(lambda x: ' '.join(dict.fromkeys(x).keys()))


        # Extract the club information from the 'Name' column and create a new 'Club' column.
        top_scorers['Club'] = top_scorers.Name.str.split().str[2:].str.join(' ')
        top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(' ')
        col = top_scorers.pop("Club")
        top_scorers.insert(2, 'Club', col)

        # The 'Club' column contains the club information, but it may have extra words. In that case we have three clubs with extra words in their names.
        top_scorers.Club = top_scorers.Club.apply(lambda x: 'Man City' if 'Man City' in x else x)
        top_scorers.Club = top_scorers.Club.apply(lambda x: 'Man Utd' if 'Man Utd' in x else x)
        top_scorers.Club = top_scorers.Club.apply(lambda x: 'Brighton & Hove Albion' if 'Brighton & Hove Albion' in x else x)
    except AttributeError: 
        print("Could not find the table element on the page. Please check the website structure.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the HTTP request: {e}")
    except TimeoutError:
        print("The request timed out. Please check your internet connection or try again later.")   

    return top_scorers




def detail_top():
    """
        This function scrapes the detailed top scorers of the Premier League from the 
        World Football website.
    """
    url = 'https://www.worldfootball.net/goalgetter/eng-premier-league-2023-2024/'
    headers = []
    
    # use the helper function to initialize the WebDriver
    driver = initialize_webdriver()


    try:
        driver.get(url)
        driver.implicitly_wait(10)
        table = driver.find_element(By.CLASS_NAME,"module-statistics.statistics")

        # Extract column headers
        for i in table.find_elements(By.TAG_NAME,'th'):
            title = i.text
            headers.append(title)
        detail_top_scorer = pd.DataFrame(columns = headers)

        # Extract row data starting at position 1 and populate the DataFrame
        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(detail_top_scorer)
            detail_top_scorer.loc[length] = row

        detail_top_scorer = detail_top_scorer.drop([''],axis=1)
        detail_top_scorer[['Player', 'Team']] = detail_top_scorer['Player'].str.split(r'\n+|\t+', regex=True, expand=True)
        detail_top_scorer.insert(2,'Team', detail_top_scorer.pop('Team'))
        detail_top_scorer.rename(columns = {'11m':' Penalty Goals'}, inplace = True)
        detail_top_scorer = detail_top_scorer.drop(['#'], axis = 1)
    except AttributeError:
        print("Could not find the table element on the page. Please check the website structure.")
    except TimeoutException:
        print("Page load timed out. Please check your internet connection or try again later.")

    finally:
        driver.quit()

    return detail_top_scorer




def all_time_table():
    """
    This function scrapes the all-time Premier League table from the World Football website.
    """
    url = 'https://www.worldfootball.net/alltime_table/eng-premier-league/pl-only/'
    headers = ['Pos', '#','Team','##', '###', 'Matches', 'Wins', 'Draws', 'Losses', 'Goals', 'Diff', 'Points']

    # use the helper function to initialize the WebDriver
    driver = initialize_webdriver()

    try:    
        driver.implicitly_wait(10)
        driver.get(url)
        table = driver.find_element(By.CSS_SELECTOR, "table[data-competition_id='91']")
        all_time_table = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(all_time_table)
            all_time_table.loc[length] = row
        
        all_time_table = all_time_table.drop(['#','##','###'],axis=1)
        all_time_table['Team'] = all_time_table['Team'].str.replace(r'\n+|\t+','', regex=True)
    except AttributeError:
        print("Could not find the table element on the page. Please check the website structure.")
    except TimeoutException:
        print("Page load timed out. Please check your internet connection or try again later.")
    finally:
        driver.quit()
    return all_time_table

def all_time_winner_club():
    """
    This function scrapes the all-time Premier League winner clubs from the World Football website.
    """
    url = 'https://www.worldfootball.net/winner/eng-premier-league/'
    headers = ['Year','','Team','Total_Titles']
     # use the helper function to initialize the WebDriver
    driver = initialize_webdriver()
    try:
        driver.implicitly_wait(10)
        driver.get(url)
        table = driver.find_element(By.TAG_NAME,"table")
        winners = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(winners)
            winners.loc[length] = row

        winners = winners.drop([''],axis=1)
        winners['Total_Titles'] = winners['Total_Titles'].str.replace(r'(|)','', regex=True)
    except AttributeError:
        print("Could not find the table element on the page. Please check the website structure.")
    except TimeoutException:
        print("Page load timed out. Please check your internet connection or try again later.")
    finally:
        driver.quit()

    return winners


def top_scorers_seasons():
    """
    This function scrapes the top scorers of the Premier League for each season from the World Football website.
    """
    url = 'https://www.worldfootball.net/top_scorer/eng-premier-league/'
    headers = ['Season', '#', 'Top scorer', 'Goals']
     # use the helper function to initialize the WebDriver
    driver = initialize_webdriver()

    try:
        driver.implicitly_wait(10)
        driver.get(url)
        table = driver.find_element(By.TAG_NAME,"table")
        top_scorer = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(top_scorer)
            top_scorer.loc[length] = row

        top_scorer = top_scorer.drop(['#'],axis=1)
        top_scorer = top_scorer.replace(r'\n+|\t+','', regex=True).astype(str)
        top_scorer['Season'] = top_scorer['Season'].replace('',np.nan).ffill()
    except AttributeError:
        print("Could not find the table element on the page. Please check the website structure.")
    except TimeoutException:
        print("Page load timed out. Please check your internet connection or try again later.")
    finally:
        driver.quit()

    return top_scorer



if __name__ == "__main__":
      print(detail_top())
