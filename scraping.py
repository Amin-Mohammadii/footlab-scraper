import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
years = list(range(2025, 2021, -1))
all_matches = []
scraper = cloudscraper.create_scraper()
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
for year in years:
    time.sleep(3)
    response = scraper.get(standings_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    standings_table = soup.select('table.stats_table')[0]
    links = [a["href"] for a in standings_table.find_all("a") if '/squads/' in a["href"]]
    team_urls = [f"https://fbref.com{l}"for l in links]

    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"
    for team_url in team_urls:
        time.sleep(3)
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = scraper.get(team_url)
        soup_team = BeautifulSoup(data.text, "html.parser")
        table = soup_team.find("table", {"id": "matchlogs_for"})
        links = soup_team.find_all('a')
        links = [l.get("href") for l in links]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        time.sleep(3)
        links = "https://fbref.com" + links[0]
        data_shooting = scraper.get(links)
        soup_shooting = BeautifulSoup(data_shooting.text, "html.parser")      
        time.sleep(3)  
        shooting_stat = soup_shooting.find("table", {"id": "matchlogs_for"})
        df_shooting = pd.read_html(str(shooting_stat))[0]
        df = pd.read_html(str(table))[0]
        df_shooting.columns = df_shooting.columns.droplevel()
        try:
            team_data = df.merge(
                df_shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]],
                on="Date",
                how="left"
            )
        except ValueError:
            continue

        team_data = team_data[team_data["Comp"] == "Premier League"]
        team_data["Season"] = year
        team_data["team"] = team_name
        all_matches.append(team_data)
        print(f"Saved data for {team_name} ({year})")

match_df = pd.concat(all_matches)
match_df.to_csv("matches.csv")





