from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from subjects.models import Subject
from django.core import serializers


def index(request):
    subjects = Subject.objects.all()
    data = serializers.serialize('json', subjects)
    return HttpResponse(data, content_type="application/json")
