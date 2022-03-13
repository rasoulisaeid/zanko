from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from points.models import Point
from django.core import serializers


def index(request):
    points = Point.objects.all()
    data = serializers.serialize('json', points)
    return HttpResponse(data, content_type="application/json")
