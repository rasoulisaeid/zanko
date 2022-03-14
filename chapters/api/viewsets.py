from chapters.models import Chapter
from .serializers import ChapterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


