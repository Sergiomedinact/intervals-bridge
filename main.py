from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

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
    headers = {"Authorization": API_KEY}
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
