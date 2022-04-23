from books.models import Book
from chapters.models import Chapter
from .serializers import BookSerializer
from chapters.api.serializers import ChapterSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from zanko.permissions import JustOwner
from auth.models import User
from studies.models import Study
import jdatetime as time
import pytz
# class OwnerOnly(BasePermission):
#   def has_permission(self, request, object):
#       return request.user == object.user()

def chapter_data(user, chapter):
    points = chapter.points.order_by('id')
    level_1, level_2, level_3, level_4, ready = 0, 0, 0, 0, 0
    for point in points:
        study = Study.objects.filter(point=point, user=user)
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
    chapter_data = level_1, level_2, level_3, level_4, ready          
    return chapter_data

def book_data(request, book):
    chapters = book.chapters.order_by('id')
    level_1, level_2, level_3, level_4, ready = 0, 0, 0, 0, 0
    for chapter in chapters:
         lvl1, lvl2, lvl3, lvl4, rdy = chapter_data(request.user, chapter)   
         level_1 += lvl1
         level_2 += lvl2
         level_3 += lvl3
         level_4 += lvl4
         ready += rdy
    book_data = str(level_1) + str(level_2) + str(level_3) + str(level_4) + str(ready)            
    return book_data

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        user = request.user
        # Each book has many chapters and we load them
        # my_books = user.book_set.prefetch_related('chapters').order_by('id')
        books = user.books.order_by('id')
        for book in books:
            book.data = book_data(request, book)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        book.name = request.data.get('name')
        book.description = request.data.get('description')
        book.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})
