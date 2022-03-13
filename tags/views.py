from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from tags.models import Tag
from django.core import serializers


def index(request):
    tags = Tag.objects.all()
    data = serializers.serialize('json', tags)
    return HttpResponse(data, content_type="application/json")
