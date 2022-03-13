from django.urls import path
from chapters.views import *

app_name = "chapters"

urlpatterns = [
    path('index', index),
]
