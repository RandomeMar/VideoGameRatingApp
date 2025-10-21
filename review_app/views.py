from django.shortcuts import render
from djangoproject import settings # TODO: Change to "from django.conf import settings"
from django.http import HttpRequest, HttpResponse
import requests


# Create your views here.
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
    