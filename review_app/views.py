from django.shortcuts import render
from djangoproject import settings # TODO: Change to "from django.conf import settings"
from django.http import HttpRequest, HttpResponse
from datetime import datetime
import requests
from review_app.models import Game, Review


# Create your views here.
def index(request: HttpRequest):
    return render(request, "search_page.html")

def search_games(request: HttpRequest):
    query = request.GET.get('q')
    
    params = {
        "key" : settings.RAWG_API_KEY,
        "search" : query,
        "page_size" : 40
    }

    response = requests.get(settings.RAWG_API_URL, params)
    if response.status_code == 200:
        # All good
        data = response.json()
        context = {
            "games": data["results"],
            "query": query
        }
        
        return render(request, "game_list.html", context)
    else:
        return HttpResponse(f"API ERROR: {response.status_code}")
    
def load_game_page(request: HttpRequest, rawg_id: int):
    name = request.GET.get("name")
    release_date = request.GET.get("released")
    if release_date:
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date() # Converts string to Date object
    img_url = request.GET.get("img_url")
    
    game: Game = Game.objects.filter(rawg_id=rawg_id).first()
    
    if not game:
        # Adds game tuple to local Game DB table
        game = Game(name=name, rawg_id=rawg_id, release_date=release_date, img_url=img_url)
        game.save()
    
    context = {"game": game}
    
    return render(request, "game_page.html", context)