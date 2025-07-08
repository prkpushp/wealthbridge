import os, requests, json, re

API_KEY = os.getenv("GEMINI_API_KEY")
SOURCE_URL = os.getenv("SOURCE_URL")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

with open("page_content-pro.txt", "r", encoding="utf-8") as f:
    content = f.read()
if len(content) > 12000:
    content = content[:12000]

prompt = (
    "Create a blog-style summary of this article.\n"
    "Start with a short <h2> introduction, then summarize in <ul>.\n"
    "Close with a readable backlink.\n\n" + content
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
except Exception:
    print("Invalid Gemini response")
    exit(1)

# Clean code block wrappers
if summary.startswith("```html"):
    summary = summary.replace("```html", "").replace("```", "").strip()

# Extract first <p> as excerpt
match = re.search(r"<p>(.*?)</p>", summary, re.DOTALL)
excerpt = match.group(1).strip() if match else "Summary from CNBC."
with open("excerpt-pro.txt", "w", encoding="utf-8") as f:
    f.write(excerpt)

# Wrap with basic styling + backlink
styled = f'''<div style="font-family:Segoe UI,Roboto,sans-serif;font-size:17px;line-height:1.7;color:#222;">
{summary}
</div>
<p><em style="font-size:15px;color:#555;">Source: <a href="{SOURCE_URL}" target="_blank" style="color:#0073aa;">{SOURCE_URL}</a></em></p>'''

with open("summary-pro.html", "w", encoding="utf-8") as f:
    f.write(styled)
