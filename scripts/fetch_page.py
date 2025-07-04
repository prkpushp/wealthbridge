import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Usage: fetch_page.py <url>")
    sys.exit(1)

url = sys.argv[1]

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Get main text content
    text = soup.get_text(separator='\n', strip=True)
    # Save to temporary file for summarization
    with open('page_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)
except Exception as e:
    print(f"Failed to fetch URL: {e}")
    sys.exit(1)
