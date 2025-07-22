# scripts/select_latest_finance_url.py
import requests
from bs4 import BeautifulSoup

url = "https://www.cnbc.com/finance/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

link = soup.select_one("a.Card-title")  # Select first featured article
if not link or not link['href']:
    raise RuntimeError("No article found on CNBC Finance page.")

article_url = link['href']
if article_url.startswith("/"):
    article_url = "https://www.cnbc.com" + article_url

with open("selected_url.txt", "w") as f:
    f.write(article_url)
