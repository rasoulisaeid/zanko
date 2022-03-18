from chapters.models import Chapter
from points.models import Point
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from zanko.permissions import JustOwner
from .serializers import PointSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class PointViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner, IsAuthenticated]
    queryset = Point.objects.all()
    serializer_class = PointSerializer


    def perform_create(self, serializer):
        chapter = Chapter.objects.get(id=self.request.data.get('chapter'))
        serializer.save(user=self.request.user, chapter=chapter)


    def list(self, request):
        # Note that we can't use request.data
        chapter_id = request.query_params.get('chapter', None)
        chapter = Chapter.objects.get(pk=chapter_id)
        # chapter = chapter.subject_set.prefetch_related('subjects').order_by('id')
        points = chapter.points.order_by('id')
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        point = self.get_object()
        point.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        point = self.get_object()
        point.explains = request.data.get('explains')
        point.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})

