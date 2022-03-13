from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from chapters.models import Chapter
from django.core import serializers


def index(request):
    chapters = Chapter.objects.all()
    data = serializers.serialize('json', chapters)
    return HttpResponse(data, content_type="application/json")
