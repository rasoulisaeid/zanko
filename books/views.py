from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from books.models import Book
from django.core import serializers


def index(request):
    books = Book.objects.all()
    data = serializers.serialize('json', books)
    return HttpResponse(data, content_type="application/json")
