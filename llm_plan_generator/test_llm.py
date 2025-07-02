import requests

payload = {
    "resume": "Python, Flask, ML basics, pandas, numpy",
    "goal": "Become a React + AI Developer",
    "time_per_day": 90
}

response = requests.post("http://127.0.0.1:5000/generate-plan", json=payload)

print("📄 Learning Plan:\n", response.json())
