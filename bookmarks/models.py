from django.db import models
from points.models import Point
from auth.models import User
from books.models import Book

class Bookmark(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return "علاقمندی ها"           

