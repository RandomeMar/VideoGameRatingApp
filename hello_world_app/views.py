from django.http import HttpResponse
from django.shortcuts import render

def hello_world(request):
    return HttpResponse("Hello World!")

def index(request):
    return render(request, "index_hello.html")

def about(request):
    return render(request, "about_hello.html")
