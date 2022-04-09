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

# class OwnerOnly(BasePermission):
#   def has_permission(self, request, object):
#       return request.user == object.user()

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
