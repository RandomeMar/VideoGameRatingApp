from django.urls import path
from review_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_games, name="search_games"),
    path("game/<int:rawg_id>/", views.load_game_page, name="load_game_page")
]