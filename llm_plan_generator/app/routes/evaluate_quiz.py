import os
import requests
import re
import json
from dotenv import load_dotenv
from app.schemas.evaluate_schema import EvaluateInput

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

def evaluate_quiz(input_data):
    validated_input = EvaluateInput(**input_data)

    prompt = f"""
You are a grading assistant.
IMPORTANT:
- Return only valid JSON.
- Do NOT include any explanation.
- Do NOT wrap in markdown.
- Respond only with JSON.

Compare the provided answers to the correct answers and return JSON like this:
{{
  "correct_count": 2,
  "total_questions": 2,
  "percentage": 100
}}

Questions:
{json.dumps(validated_input.questions, indent=2)}

User Answers:
{json.dumps(validated_input.answers, indent=2)}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.3,
        "top_p": 0.9,
        "stop": ["</s>"]
    }

    response = requests.post("https://api.together.xyz/inference", json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error from Together.ai: {response.text}")

    output_text = response.json()['output']['choices'][0]['text']

    # Remove any markdown or explanation
    matches = re.findall(r"{.*}", output_text, re.DOTALL)
    if not matches:
        raise Exception(f"JSON parsing error: No JSON found.\nOutput was:\n{output_text}")

    json_text = matches[0]

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise Exception(f"JSON parsing error: {e}\nExtracted text:\n{json_text}")

    # Return your desired format
    return {
        "score": f"{parsed['percentage']}%",
        "details": {
            "correct_count": parsed["correct_count"],
            "total_questions": parsed["total_questions"]
        }
    }
