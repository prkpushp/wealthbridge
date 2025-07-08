# scripts/fetch_page.py

import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python fetch_page.py <URL>")
    sys.exit(1)

url = sys.argv[1]

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

soup = BeautifulSoup(response.text, "lxml")

# CNBC-specific article body container
article_div = soup.find("div", class_="ArticleBody-articleBody")

if not article_div:
    print("Could not find article content")
    sys.exit(1)

# Extract and clean paragraphs
paragraphs = article_div.find_all("p")
html_content = ""
for p in paragraphs:
    text = p.get_text(strip=True)
    if text:
        html_content += f"<p>{text}</p>\n"

# Final validation
if not html_content.strip():
    print("Article content is empty")
    sys.exit(1)

# Save to file
with open("page_content.txt", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Page content saved to page_content.txt")
