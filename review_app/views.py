from django.shortcuts import render, redirect, get_object_or_404
from djangoproject import settings # TODO: Change to "from django.conf import settings"
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from datetime import datetime
import requests
from review_app.models import Game, Review
from urllib.parse import unquote


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
    game: Game = Game.objects.filter(rawg_id=rawg_id).first() or create_game(rawg_id)
    
    reviews = Review.objects.filter(game_id=game.id)
    
    context = {
        "game": game,
        "reviews": reviews
    }
    
    return render(request, "game_page.html", context)

def create_game(rawg_id: int):
    params = {"key" : settings.RAWG_API_KEY}
    url = f"{settings.RAWG_API_URL}/{rawg_id}"
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # All good
        data: dict = response.json()
        release_date = data.get("released")
        if release_date:
            release_date = datetime.strptime(release_date, "%Y-%m-%d")
        game = Game(name=data["name"], rawg_id=data["id"], release_date=release_date, img_url=data.get("background_image"))
        game.save()
        return game
    else:
        return HttpResponse(f"API ERROR: {response.status_code}")
  

def load_review_form(request: HttpRequest, game_id: int):
    game = get_object_or_404(Game, id=game_id)
    review_id = request.GET.get("review_id")
    context = {"game": game}
    if review_id:
        context["review"] = Review.objects.filter(id=review_id).first()
    
    return render(request, "review_form.html", context)


def create_review(request: HttpRequest, game_id: int):
    review_id = request.POST.get("review_id")
    title = request.POST.get("title")
    review_text = request.POST.get("review_text")
    rating = request.POST.get("rating")
    nickname = request.POST.get("nickname")
    
    review: Review = Review.objects.filter(id=review_id).first()
    
    if not review:
        game = get_object_or_404(Game, id=game_id)
        review = Review(game=game)
      
    review.review_text = review_text
    review.rating = int(rating)
    review.title = title
    review.nickname = nickname
    review.save()
    
    return render(request, "confirmation_page.html", {"review": review})


def auth_edit_code(request: HttpRequest, review_id: int):
    review: Review = get_object_or_404(Review, id=review_id)
    
    edit_code = request.POST.get("edit_code")
    action = request.POST.get("action")
    
    if not edit_code:
        return render(request, "edit_code_form.html", {"review_id": review_id})
    
    if edit_code != review.edit_code:
        # Wrong edit code
        return render(request, "edit_code_form.html", {"review_id": review_id, "error": "Wrong code. Try again."})
    
    if action == "edit":
        # Edit
        url = f"{reverse("load_review_form", args=[review.game.id])}?review_id={review_id}"
        return redirect(url)
    elif action == "delete":
        # Delete
        rawg_id = review.game.rawg_id
        review.delete()
        return redirect("load_game_page", rawg_id=rawg_id)
    else:
        return render(request, "edit_code_form.html", {"review_id": review_id, "error": "An invalid action was selected"})
        
    