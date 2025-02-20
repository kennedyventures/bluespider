from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BLUESKY_API = "https://bsky.social/xrpc"

def fetch_lists(user_handle):
    """ Fetch public lists from a Bluesky user """
    url = f"{BLUESKY_API}/app.bsky.graph.getLists?actor={user_handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("lists", [])
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
