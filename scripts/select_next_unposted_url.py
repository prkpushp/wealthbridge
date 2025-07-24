import requests
from bs4 import BeautifulSoup

CNBC_FINANCE_URL = "https://www.cnbc.com/finance/"
POSTED_LOG = "uploaded_url.txt"

# Read already uploaded URLs
try:
    with open(POSTED_LOG, "r") as f:
        uploaded = set(line.strip() for line in f)
except FileNotFoundError:
    uploaded = set()

# Fetch CNBC finance page
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(CNBC_FINANCE_URL, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")
links = soup.select('a[href^="https://www.cnbc.com/"]')

# Filter only article URLs ending in .html
urls = [link.get("href").split("?")[0] for link in links if link.get("href", "").endswith(".html")]

# Select first new article
for url in urls:
    if url not in uploaded:
        with open("selected_url.txt", "w") as f:
            f.write(url)
        print(f"✅ Selected new URL: {url}")
        break
else:
    print("❌ No new unposted CNBC article found.")
    exit(1)
