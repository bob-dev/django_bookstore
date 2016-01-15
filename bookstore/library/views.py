from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    text = "First view"
    return HttpResponse(text)