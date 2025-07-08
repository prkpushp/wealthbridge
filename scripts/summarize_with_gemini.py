import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY")
SOURCE_URL = os.environ.get("SOURCE_URL")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

with open('page_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

if len(content) > 12000:
    content = content[:12000]

prompt = (
    "Create a blog-style summary of this article.\n"
    "Start with a short introduction (<h2>), then summarize the main points in an HTML <ul> list.\n"
    "End with a clean backlink to the original article.\n\n"
    + content
)

response = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-001:generateContent?key={API_KEY}",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 512}
    })
)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit(1)

try:
    summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
except (KeyError, IndexError):
    print("Invalid Gemini response")
    exit(1)

# Remove Markdown code block wrappers if present
if summary.startswith("```html"):
    summary = summary.replace("```html", "").replace("```", "").strip()

# Extract first paragraph as excerpt
import re
match = re.search(r"<p>(.*?)</p>", summary, re.DOTALL)
excerpt = match.group(1).strip() if match else "A concise summary of today's market insights from CNBC."

# Save excerpt
with open("excerpt.txt", "w", encoding="utf-8") as f:
    f.write(excerpt)

# Wrap summary with styled container
styled_summary = f'''
<div style="font-family: 'Segoe UI', Roboto, sans-serif; font-size: 17px; line-height: 1.7; color: #222; padding: 10px 0;">
{summary}
</div>
<p><em style="font-size: 15px; color: #555;">Source: <a href="{SOURCE_URL}" target="_blank" style="color: #0073aa;">{SOURCE_URL}</a></em></p>
'''

# Save styled HTML
with open("summary.html", "w", encoding="utf-8") as f:
    f.write(styled_summary)
