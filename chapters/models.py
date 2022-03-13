from django.db import models
from books.models import Book

class Chapter(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.name

    def get_book(self):
        return self.book.name
        
            


