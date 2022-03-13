from chapters.models import Chapter
from .serializers import ChapterSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @action(methods=['GET'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('created_date').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

