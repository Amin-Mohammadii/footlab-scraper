import requests
from bs4 import BeautifulSoup
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(standings_url)
print(data.text)

