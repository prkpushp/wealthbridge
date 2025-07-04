import os
import google.generativeai as genai

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

# Read the fetched content
with open('page_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Truncate if content is too long for Gemini's prompt
max_input_length = 12000  # adjust according to Gemini model limits
if len(content) > max_input_length:
    content = content[:max_input_length]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

prompt = (
    "Summarize the following text in concise bullet points or a short paragraph:\n\n"
    + content
)

response = model.generate_content(prompt)

with open('summary.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
