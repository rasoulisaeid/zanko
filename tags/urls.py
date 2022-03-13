from django.urls import path
from tags.views import *

app_name = "tags"

urlpatterns = [
    path('index', index),
]
