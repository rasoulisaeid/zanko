from django.db import models
from auth.models import User
from books.models import Book

class Purchase(models.Model):
    description = models.CharField(blank=True, null=True, max_length=255)
    price = models.IntegerField()
    user = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="purchases", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.book.name

