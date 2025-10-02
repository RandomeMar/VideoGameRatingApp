from django.urls import path
from hello_world_app import views

urlpatterns = [
    path("example/", views.index, name="index"),
    path("example/about/", views.about, name="about"),]