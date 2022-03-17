from subjects.models import Subject
from chapters.models import Chapter
from .serializers import SubjectSerializer
from chapters.api.serializers import ChapterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

