from django.urls import path
from review_app import views

path("search/", views.search_games, name="search_games")