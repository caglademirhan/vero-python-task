from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.baubuddy.de/dev/index.php/v1"
LABEL_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}"

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if file:
            # Read CSV data
            csv_data = pd.read_csv(file, delimiter=";")
            
            # Get resources from the Baubuddy API
            resources = get_resources(csv_data)
            
            # Filter resources based on 'hu' field
            filtered_resources = filter_resources(resources)

            # Resolve color codes for labelIds
            resolve_label_colors(filtered_resources)

            # Return the result in JSON format
            return jsonify(filtered_resources)
        else:
            return 'No file received.', 406
    except Exception as e:
        print(f"Error: {str(e)}")
        return 'Server error.', 500

def get_resources(csv_data):
    access_token = get_access_token()
    url = f"{BASE_URL}/vehicles/select/active"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"csv_data": csv_data.to_dict(orient="records")}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def filter_resources(resources):
    return [resource for resource in resources if resource.get('hu')]

def resolve_label_colors(resources):
    for resource in resources:
        label_ids = resource.get('labelIds', [])
        if label_ids:
            color_code = get_label_color(label_ids[0])
            resource['labelColor'] = color_code

def get_label_color(label_id):
    url = LABEL_URL.format(labelId=label_id)
    response = requests.get(url)
    color_code = response.json().get('colorCode', '')
    return color_code

def get_access_token():
    payload = {"username": "365", "password": "1"}
    response = requests.post("https://api.baubuddy.de/index.php/login", json=payload, headers={
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json",
    })
    access_token = response.json()["oauth"]["access_token"]
    return access_token

if __name__ == '__main__':
    app.run(port=3000)


