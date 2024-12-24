import requests
from bs4 import BeautifulSoup

def scrape_supplementary_data(query):
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return "No supplementary data found."
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    supplementary_data = ""
    for para in paragraphs[:3]:  # Limit to the first 3 paragraphs
        supplementary_data += para.text
    return supplementary_data
