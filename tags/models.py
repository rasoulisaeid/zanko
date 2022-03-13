from django.db import models
from auth.models import User
from points.models import Point

class Tag(models.Model):
    name = models.CharField(max_length=255)
    point = models.ManyToManyField(Point)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.name       

