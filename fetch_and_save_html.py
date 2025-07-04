import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 3:
    print("Usage: fetch_and_save_html.py <url> <output_html_file>")
    sys.exit(1)

url = sys.argv[1]
output_file = sys.argv[2]

resp = requests.get(url, timeout=15)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# Try to extract the main article if possible, else all body
article = soup.find("article")
if article:
    html_content = article.prettify()
else:
    body = soup.body
    html_content = body.prettify() if body else soup.prettify()

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)
