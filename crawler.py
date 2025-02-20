import requests

BLUESKY_API = "https://bsky.social/xrpc"

def fetch_lists(user_handle):
    """ Fetch public lists from a Bluesky user """
    url = f"{BLUESKY_API}/app.bsky.graph.getLists?actor={user_handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("lists", [])
    return []

if __name__ == "__main__":
    test_user = "example.bsky.social"
    print(fetch_lists(test_user))
