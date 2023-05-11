import requests
from bs4 import BeautifulSoup


def get_web_text(url):
    response = requests.get(url)

    # fix encoding
    response.encoding = response.apparent_encoding

    html = response.text

    # Extract all text
    soup = BeautifulSoup(html)
    text = soup.get_text()

    return text
