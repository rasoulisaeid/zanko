from django.urls import path
from subjects.views import *

app_name = "subjects"

urlpatterns = [
    path('index', index),
]
