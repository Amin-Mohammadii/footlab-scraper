import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
html = scraper.get("https://fbref.com/en/comps/9/Premier-League-Stats").text

soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())
