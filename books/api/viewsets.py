from books.models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(methods=['GET'], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by('created_date').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

