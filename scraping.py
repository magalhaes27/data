import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def league_table():
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table',class_='ssrcss-5o3au1-Table e13j9mpy3')

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    
    league_table = pd.DataFrame(columns = headers)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(league_table)
        league_table.loc[length] = row

    league_table[['Position', 'Team']] = league_table['Team'].str.extract(r'(\d+)([A-Za-z]+)')
    league_table.insert(0, 'Position', league_table.pop('Position'))
    
    league_table.drop(['Form, Last 6 games, Oldest first'], axis=1, inplace=True)

    return league_table


def top_scorers():
    url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table',class_='ssrcss-13lk35i-TableWrapper e1icz102')

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    
    top_scorers = pd.DataFrame(columns = headers)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(top_scorers)
        top_scorers.loc[length] = row

    
    top_scorers.Name = top_scorers.Name.replace(r'([A-Z])', r' \1', regex=True).str.split()
    top_scorers.Name = top_scorers.Name.apply(lambda x: ' '.join(dict.fromkeys(x).keys()))

    top_scorers['Club'] = top_scorers.Name.str.split().str[2:].str.join(' ')
    top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(' ')
    col = top_scorers.pop("Club")
    top_scorers.insert(2, 'Club', col)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Man City' if 'Man City' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Man Utd' if 'Man Utd' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Brighton & Hove Albion' if 'Brighton & Hove Albion' in x else x)

    return top_scorers

def detail_top():
    url = 'https://www.worldfootball.net/goalgetter/eng-premier-league-2023-2024/'
    headers = []
    # Set up Selenium WebDriver with options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)


    try:
        driver.get(url)
        driver.implicitly_wait(5)
        table = driver.find_element(By.CLASS_NAME,"standard_tabelle")

        for i in table.find_elements(By.TAG_NAME,'th'):
            title = i.text
            headers.append(title)
        detail_top_scorer = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(detail_top_scorer)
            detail_top_scorer.loc[length] = row

        detail_top_scorer = detail_top_scorer.drop([''],axis=1)
        detail_top_scorer['Team'] = detail_top_scorer['Team'].str.replace(r'\n+|\t+','', regex=True)
        detail_top_scorer['Penalty'] = detail_top_scorer['Goals (Penalty)'].str.split().str[-1:].str.join(' ')
        detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace('(','')
        detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace(')','')
        detail_top_scorer['Goals (Penalty)'] = detail_top_scorer['Goals (Penalty)'].str.split().str[0].str.join('')
        detail_top_scorer.rename(columns = {'Goals (Penalty)':'Goals'}, inplace = True)
        detail_top_scorer = detail_top_scorer.drop(['#'], axis = 1)
    finally:
        driver.quit()

    return detail_top_scorer


def player_table():
    url = [f'https://www.worldfootball.net/players_list/eng-premier-league-2023-2024/nach-name/{i:d}' for i in (range(1,12))]
    header = ['Player','','Team', 'born', 'Height', 'Position']
    df = pd.DataFrame(columns = header)

    def player(ev):
        url = ev
        headers = []
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.implicitly_wait(2)
            driver.get(url)
            table = driver.find_element(By.CLASS_NAME,"standard_tabelle")

            for i in table.find_elements(By.TAG_NAME,'th'):
                title = i.text
                headers.append(title)
            players = pd.DataFrame(columns = headers)

            for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
                row_data = j.find_elements(By.TAG_NAME,'td')
                row = [i.text for i in row_data]
                length = len(players)
                players.loc[length] = row
        finally:
            driver.quit()
        return players
    
    for i in url:
        data = player(i)
        df = pd.concat([df, data], axis=0).reset_index(drop=True)
    
    df = df.drop([''],axis=1)

    return df

def all_time_table():
    url = 'https://www.worldfootball.net/alltime_table/eng-premier-league/pl-only/'
    headers = ['Pos', '#', 'Team', 'Matches', 'Wins', 'Draws', 'Losses', 'Goals', 'Dif', 'Points']

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    try:    
        driver.implicitly_wait(2)
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME,"standard_tabelle")
        all_time_table = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(all_time_table)
            all_time_table.loc[length] = row
        
        all_time_table = all_time_table.drop(['#'],axis=1)
        all_time_table['Team'] = all_time_table['Team'].str.replace(r'\n+|\t+','', regex=True)
    finally:
        driver.quit()
    return all_time_table

def all_time_winner_club():
    url = 'https://www.worldfootball.net/winner/eng-premier-league/'
    headers = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.implicitly_wait(2)
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME,"standard_tabelle")

        for i in table.find_elements(By.TAG_NAME,'th'):
            title = i.text
            headers.append(title)
        winners = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(winners)
            winners.loc[length] = row

        winners = winners.drop([''],axis=1)
        winners['Year'] = winners['Year'].str.replace(r'\n+|\t+','', regex=True)
    finally:
        driver.quit()

    return winners


def top_scorers_seasons():
    url = 'https://www.worldfootball.net/top_scorer/eng-premier-league/'
    headers = ['Season', '#', 'Top scorer', '#', 'Team', 'Goals']
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.implicitly_wait(2)
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME,"standard_tabelle")
        top_scorer = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(top_scorer)
            top_scorer.loc[length] = row

        top_scorer = top_scorer.drop(['#'],axis=1)
        top_scorer = top_scorer.replace(r'\n+|\t+','', regex=True).astype(str)
        top_scorer['Season'] = top_scorer['Season'].replace('',np.nan).ffill()
    finally:
        driver.quit()

    return top_scorer

def goals_per_season():
    url = 'https://www.worldfootball.net/stats/eng-premier-league/1/'
    headers = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.implicitly_wait(2)
        driver.get(url)
        table = driver.find_element(By.CLASS_NAME,"standard_tabelle")

        for i in table.find_elements(By.TAG_NAME,'th'):
            title = i.text
            headers.append(title)
        goals_per_season = pd.DataFrame(columns = headers)

        for j in table.find_elements(By.TAG_NAME,'tr')[1:]:
            row_data = j.find_elements(By.TAG_NAME,'td')
            row = [i.text for i in row_data]
            length = len(goals_per_season)
            goals_per_season.loc[length] = row
        goals_per_season.drop(goals_per_season.index[-1], inplace=True)
        goals_per_season = goals_per_season.drop(['#'],axis=1)
        goals_per_season.rename(columns = {'goals': 'Goals', 'Ø goals':'Average Goals'}, inplace = True)
    finally:
        driver.quit()

    return goals_per_season



if __name__ == "__main__":
      print(player_table())
