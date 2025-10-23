from django.urls import path
from review_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_games, name="search_games"),
    path("game/<int:rawg_id>/", views.load_game_page, name="load_game_page"),
    path("review/<int:game_id>/", views.load_review_form, name="load_review_form"),
    path("review/<int:game_id>/confirmation/", views.create_review, name="create_review"),
    path("auth-edit-code/<int:review_id>/",views.auth_edit_code, name="auth_edit_code")
]