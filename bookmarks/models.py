from django.db import models
from points.models import Point
from favorites.models import Favorite

class Bookmark(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return "علاقمندی ها"           

