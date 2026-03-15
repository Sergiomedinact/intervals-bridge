from flask import Flask, jsonify, request
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")
BASE_URL = "https://intervals.icu/api/v1"

@app.route("/")
def home():
    return jsonify({"message": "Puente activo 🚴‍♂️"})

@app.route("/activities")
def get_activities():
    oldest = request.args.get("oldest")
    newest = request.args.get("newest")
    url = f"{BASE_URL}/athlete/{ATHLETE_ID}/activities?oldest={oldest}"
    if newest:
        url += f"&newest={newest}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route("/create_event", methods=["POST"])
def create_event():
    data = request.json
    start_date = data.get("start_date", "")
    if start_date and len(start_date) == 10:
        start_date = start_date + "T00:00:00"
    payload = {
        "start_date_local": start_date,
        "name": data.get("name"),
        "category": data.get("category", "WORKOUT"),
        "type": data.get("type", "Ride"),
        "moving_time": data.get("duration_seconds"),
        "icu_training_load": data.get("training_load"),
        "description": data.get("description", "")
    }
    url = f"{BASE_URL}/athlete/{ATHLETE_ID}/events"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return jsonify({
        "status": response.status_code,
        "data": response.json() if response.status_code in [200, 201] else response.text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Y el `requirements.txt` tiene que tener estas tres líneas:
```
flask
requests
flask-cors
