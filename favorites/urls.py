from django.urls import path
from favorites.views import *

app_name = "favorites"

urlpatterns = [
    path('index', index),
]
