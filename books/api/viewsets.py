from books.models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


    @action(methods=['GET'], detail=False)
    def index(self, request):
        user = request.user
        my_books = user.book_set.order_by('id')
        serializer = BookSerializer(my_books, many=True)
        return Response(serializer.data)
    
