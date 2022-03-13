from django.urls import path
from bookmarks.views import *

app_name = "booksmarks"

urlpatterns = [
    path('index', index),
]
