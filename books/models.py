from django.db import models
from auth.models import User

class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, default="0+0")
    active = models.BooleanField(default=False)
    sample = models.CharField(max_length=255, default="1")
    user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.name

