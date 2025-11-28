import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
response = scraper.get(standings_url)


# Parse it
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data as usual
# tables = soup.find_all('table')
# print(f"Found {len(tables)} tables")
standings_table = soup.select('table.stats_table')[0]
links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]   
team_urls = [f"https://fbref.com{l}" for l in links]
print(team_urls)

import csv

with open("links.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for item in team_urls:
        writer.writerow([item])
