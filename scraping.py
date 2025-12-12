import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

scraper = cloudscraper.create_scraper()
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

response = scraper.get(standings_url)
soup = BeautifulSoup(response.text, 'html.parser')
standings_table = soup.select('table.stats_table')[0]

links = [a["href"] for a in standings_table.find_all("a") if '/squads/' in a["href"]]
team_url = "https://fbref.com" + links[0]
team_page = scraper.get(team_url)
soup_team = BeautifulSoup(team_page.text, "html.parser")
table = soup_team.find("table", {"id": "matchlogs_for"})
        
df = pd.read_html(str(table))[0]
print(df.shape)
