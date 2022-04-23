from chapters.models import Chapter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from books.models import Book
from zanko.permissions import JustOwner
from .serializers import ChapterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from studies.models import Study
import jdatetime as time
import pytz

def chapter_data(request, chapter):
    points = chapter.points.order_by('id')
    level_1, level_2, level_3, level_4, ready = 0, 0, 0, 0, 0
    for point in points:
        study = Study.objects.filter(point=point, user=request.user)
        if study:
            level = study[0].level
            next_time = study[0].order.split("+")[-1]
            is_ready = time.datetime.strptime(next_time, "%Y-%m-%d %H:%M:%S") < time.datetime.now(pytz.timezone('Asia/Tehran'))  
            if is_ready:
                ready += 1
            if level == 1:
                level_1 += 1
            elif level == 2:
                level_2 += 1
            elif level == 3:
                level_3 += 1
            elif level == 4:
                level_4 += 1 
    chapter_data = str(level_1) + str(level_2) + str(level_3) + str(level_4) + str(ready)           
    return chapter_data

class ChapterViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner, IsAuthenticated]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.request.data.get('book'))
        serializer.save(user=self.request.user, book=book)


    def list(self, request):
        # Note that we can't use request.data
        book_id = request.query_params.get('book', None)
        book = Book.objects.get(pk=book_id)
        # chapter = chapter.subject_set.prefetch_related('subjects').order_by('id')
        chapters = book.chapters.order_by('id')
        for chapter in chapters:
            chapter.data = chapter_data(request, chapter)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        chapter = self.get_object()
        chapter.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        chapter = self.get_object()
        chapter.name = request.data.get('name')
        chapter.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})

