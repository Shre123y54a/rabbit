import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_quiz(topic):
    prompt = f"""
You are an AI tutor creating quizzes.
IMPORTANT:
- Respond only with valid JSON.
- Do NOT include any explanation or formatting.
- Provide exactly 20 questions:
  - 8 easy
  - 8 medium
  - 4 hard

Format:
[
  {{
    "question": "",
    "difficulty": "easy/medium/hard",
    "options": ["A", "B", "C", "D"],
    "answer": "A/B/C/D"
  }}
]
Topic: {topic}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/Meta-Llama-3.3-70B-Instruct-Turbo-Free",
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["</s>"]
    }

    response = requests.post(
        "https://api.together.xyz/inference",
        json=body,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.text}")

    output_text = response.json()["output"]["choices"][0]["text"]

    matches = re.findall(r"\[\s*{.*}\s*\]", output_text, re.DOTALL)
    if not matches:
        raise Exception(f"No JSON array found:\n{output_text}")
    json_text = matches[0]

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise Exception(f"JSON parse error: {e}\n{json_text}")

    return parsed
