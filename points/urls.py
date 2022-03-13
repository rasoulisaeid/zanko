from django.urls import path
from points.views import *

app_name = "points"

urlpatterns = [
    path('index', index),
]
