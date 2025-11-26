import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
response = scraper.get(standings_url)

# Now you have the HTML
html_content = response.text

# Parse it
soup = BeautifulSoup(html_content, 'html.parser')
# Extract data as usual
# tables = soup.find_all('table')
# print(f"Found {len(tables)} tables")
print(soup.prettify())