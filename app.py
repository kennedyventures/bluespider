from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BLUESKY_API = "https://bsky.social/xrpc"

import json
import os
import requests

BLUESKY_API = "https://bsky.social/xrpc"

def get_auth_token():
    """ Authenticate with Bluesky and get an access token """
    login_url = f"{BLUESKY_API}/com.atproto.server.createSession"
    credentials = {
        "identifier": os.getenv("BSKY_USERNAME"),
        "password": os.getenv("BSKY_APP_PASSWORD")
    }
    response = requests.post(login_url, json=credentials)

    if response.status_code == 200:
        return response.json().get("accessJwt")
    else:
        print(f"Bluesky login failed: {response.text}")
        return None

def fetch_lists(user_handle):
    """ Fetch public lists from a Bluesky user with authentication """
    auth_token = get_auth_token()
    if not auth_token:
        return {"error": "Failed to authenticate with Bluesky"}

    url = f"{BLUESKY_API}/app.bsky.graph.getLists?actor={user_handle}"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)

    print(f"Fetching lists for {user_handle}: Status {response.status_code}")
    print(f"Full Response: {response.text}")

    if response.status_code == 200:
        try:
            return response.json().get("lists", [])
        except json.JSONDecodeError:
            print("Error decoding JSON response from Bluesky")
            return []
    return []



@app.route('/')
def home():
    return "Bluesky List Crawler is running!"

@app.route('/crawl', methods=['GET'])
def crawl():
    """ API endpoint to fetch lists from a Bluesky user """
    user_handle = request.args.get('user', 'example.bsky.social')  # Default user if none provided
    lists = fetch_lists(user_handle)
    return jsonify({"user": user_handle, "lists": lists})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
