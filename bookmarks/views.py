from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bookmarks.models import Bookmark
from django.core import serializers


def index(request):
    bookmarks = Bookmark.objects.all()
    data = serializers.serialize('json', bookmarks)
    return HttpResponse(data, content_type="application/json")
