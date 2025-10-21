import requests

API_KEY = "849b97a03cb04649a27a482ac716bb86"

url = "https://api.rawg.io/api/games"


query = "elden ring"

params = {
    "key" : API_KEY,
    "search" : query,
    "page_size" : 40
}

response = requests.get(url, params)
if response.status_code == 200:
    # All good
    data = response.json()
    games = data["results"]
    for game in games:
        print(f"Title: {game["name"]}")
        print(f"ID: {game["id"]}")
        print(f"Release: {game["released"]}")
        print(f"Image URL: {game["background_image"]}\n")
else:
    print(f"API Error: {response.status_code}")