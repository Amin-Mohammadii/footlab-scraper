import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time
# scraper = cloudscraper.create_scraper()
# standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# response = scraper.get(standings_url)
# soup = BeautifulSoup(response.text, 'html.parser')
# standings_table = soup.select('table.stats_table')[0]

# links = [a["href"] for a in standings_table.find_all("a") if '/squads/' in a["href"]]
# team_url = "https://fbref.com" + links[0]
# team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
# print(team_name)
# team_page = scraper.get(team_url)
# soup_team = BeautifulSoup(team_page.text, "html.parser")
# table = soup_team.find("table", {"id": "matchlogs_for"})
# df = pd.read_html(str(table))[0]
# print(df)
years = list(range(2025, 2023, -1))
all_matches = []
scraper = cloudscraper.create_scraper()
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
for year in years:
    response = scraper.get(standings_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    standings_table = soup.select('table.stats_table')[0]
    links = [a["href"] for a in standings_table.find_all("a") if '/squads/' in a["href"]]
    team_urls = [f"https://fbref.com{l}"for l in links]
    for team_url in team_urls:
        time.sleep(5)
        
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = scraper.get(team_url)
        soup_team = BeautifulSoup(data.text, "html.parser")
        table = soup_team.find("table", {"id": "matchlogs_for"})
        df = pd.read_html(str(table))[0]
        print(df)
        
df.to_csv("matches.csv")

