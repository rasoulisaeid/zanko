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
from purchases.models import Purchase
import jdatetime as time
import pytz
# class OwnerOnly(BasePermission):
#   def has_permission(self, request, object):
#       return request.user == object.user()

def chapter_data(user, chapter):
    points = chapter.points.order_by('id')
    level_1, level_2, level_3, level_4, level_5, ready = 0, 0, 0, 0, 0, 0
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
            elif level == 5:
                level_5 += 1     
    chapter_data = level_1, level_2, level_3, level_4, level_5, ready          
    return chapter_data

def book_data(request, book):
    chapters = book.chapters.order_by('id')
    level_1, level_2, level_3, level_4, level_5, ready = 0, 0, 0, 0, 0, 0
    for chapter in chapters:
         lvl1, lvl2, lvl3, lvl4, lvl5, rdy = chapter_data(request.user, chapter)   
         level_1 += lvl1
         level_2 += lvl2
         level_3 += lvl3
         level_4 += lvl4
         level_5 += lvl5
         ready += rdy
    book_data = str(level_1) + "_" + str(level_2) + "_" + str(level_3) + "_" + str(level_4) + "_" + str(level_5) + "_" + str(ready)            
    return book_data

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.staff:
            serializer.save(user=self.request.user)
        else:
            return Response(data=[{'status': status.HTTP_200_OK, "message":'not-staff'}])     
        
    def list(self, request):
        user = request.user
        body = request.GET.get('body')
        store = body.split('_')[0]
        if store == "yes":
            books = Book.objects.filter(active=True)
            category = body.split('_')[1]
            books_list = [] 
            for book in books:
                writer = User.objects.get(pk=book.user.id)
                if book.category == category:
                    book.data = writer.name
                    book.purchased = False
                    purachased = Purchase.objects.filter(user=user, book=book)
                    if purachased:
                        book.purchased = True
                    books_list.append(book)
            serializer = BookSerializer(books_list, many=True)
            return Response({'books':serializer.data})        
        else:
            if user.staff:
                books = user.books.order_by('id')
                for book in books:
                    book.data = book_data(request, book)
                    book.purchased = False
                serializer = BookSerializer(books, many=True)
                return Response({'books':serializer.data, 'balance':user.balance, 'staff':True})
            else:
                purchased = Purchase.objects.filter(user=user)
                purchased_books = []
                for item in purchased:
                    book = Book.objects.get(pk=item.book.id)
                    book.data = book_data(request, book)
                    book.purchased = True
                    purchased_books.append(book)
                serializer = BookSerializer(purchased_books, many=True)
                return Response({'books':serializer.data, 'balance':user.balance, 'staff':False})
           

   
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
