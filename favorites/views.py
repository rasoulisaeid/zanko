from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from favorites.models import Favorite
from django.core import serializers


def index(request):
    favorites = Favorite.objects.all()
    data = serializers.serialize('json', favorites)
    return HttpResponse(data, content_type="application/json")
