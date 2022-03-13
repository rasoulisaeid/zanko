from django.urls import path
from books.views import *

app_name = "books"

urlpatterns = [
    path('index', index),
    # path('books/save', save_book , name="saveBook"),
]
