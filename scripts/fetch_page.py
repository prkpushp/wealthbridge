# scripts/fetch_page.py

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

if len(sys.argv) < 2:
    print("Usage: python fetch_page.py <URL>")
    sys.exit(1)

url = sys.argv[1]
domain = urlparse(url).netloc

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch URL: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

text = ""

# --- SITE-SPECIFIC PARSING RULES ---

if "cnbc.com" in domain:
    article = soup.find("div", class_="ArticleBody-articleBody")
    if article:
        paragraphs = article.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

elif "indiatimes.com" in domain:
    article = soup.find("div", class_="article-content") or soup.find("div", {"class": lambda x: x and "content" in x})
    if article:
        paragraphs = article.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

# --- GENERAL FALLBACK ---

if not text:
    article = soup.find("article") or soup.find("main")
    if article:
        paragraphs = article.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

# --- Final Check ---

if not text.strip():
    print("Could not find article content")
    sys.exit(1)

with open("page_content.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Page content saved to page_content.txt")
