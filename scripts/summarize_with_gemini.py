import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

# Read the page content to summarize
with open('page_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Truncate if too long for Gemini's prompt
max_input_length = 12000
if len(content) > max_input_length:
    content = content[:max_input_length]

prompt = (
    "Summarize the following text in concise bullet points or a short paragraph:\n\n"
    + content
)

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.3,
        "maxOutputTokens": 512
    }
}

response = requests.post(API_URL, headers=headers, data=json.dumps(data))
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit(1)

resp_json = response.json()
try:
    summary = resp_json["candidates"][0]["content"]["parts"][0]["text"]
except (KeyError, IndexError):
    print("Unexpected response format:", resp_json)
    exit(1)

with open('summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)
