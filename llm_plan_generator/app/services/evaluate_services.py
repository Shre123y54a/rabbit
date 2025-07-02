import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

def evaluate_quiz(input_data):
    questions = input_data.get("questions")
    answers = input_data.get("answers")

    prompt = f"""
You are an expert evaluator.

Given the following questions and user answers, return a JSON object with:
- "correct_count": number of correct answers
- "total_questions": total number of questions
- "percentage": accuracy percentage (0-100)

Questions and Answers:
{json.dumps(questions, indent=2)}

User Answers:
{json.dumps(answers, indent=2)}

IMPORTANT:
Respond ONLY with valid JSON in this format:
{{
  "correct_count": 0,
  "total_questions": 0,
  "percentage": 0
}}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0,
        "stop": ["</s>"]
    }

    response = requests.post("https://api.together.xyz/inference", json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error from Together.ai: {response.text}")

    output_text = response.json()['output']['choices'][0]['text']

    matches = re.findall(r"\{.*\}", output_text, re.DOTALL)
    if not matches:
        raise Exception(f"No JSON found:\n{output_text}")

    json_text = matches[0]

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise Exception(f"JSON parse error: {e}\nExtracted:\n{json_text}")

    return parsed
