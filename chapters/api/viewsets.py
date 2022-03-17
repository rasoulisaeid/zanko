from chapters.models import Chapter
from subjects.models import Subject
from django.shortcuts import get_object_or_404
from books.models import Book
from zanko.permissions import JustOwner
from .serializers import ChapterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class ChapterViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner]
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

