import sys
import requests
from bs4 import BeautifulSoup
import json

if len(sys.argv) < 2:
    print("Usage: python fetch_page.py <URL>")
    sys.exit(1)

url = sys.argv[1]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
except Exception as e:
    print(f"Failed to fetch URL: {e}")
    sys.exit(1)

soup = BeautifulSoup(res.text, "html.parser")

# Extract article body (CNBC-specific)
body = soup.find("div", class_="ArticleBody-articleBody")
if not body:
    print("Could not find article content")
    sys.exit(1)

html_content = ""
for p in body.find_all("p"):
    text = p.get_text(strip=True)
    if text:
        html_content += f"<p>{text}</p>\n"

# Save article content
with open("page_content.txt", "w", encoding="utf-8") as f:
    f.write(html_content)

# Extract metadata
title = soup.find("h1")
image_div = soup.find("div", class_="ArticleHeader-heroImage")
image_url = image_div.img["src"] if image_div and image_div.img else None

with open("meta.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": title.get_text(strip=True) if title else None,
        "image": image_url
    }, f)
