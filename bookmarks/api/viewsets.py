from bookmarks.models import Bookmark
from points.models import Point
from .serializers import BookmarkSerializer
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

def find_book(point):
    chapter = point.chapter
    return chapter.book

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        point = Point.objects.get(id=self.request.data.get('point'))
        user = self.request.user
        bookmark = Bookmark.objects.filter(user=user, point=point).first()
        if bookmark:
            bookmark.delete()
            return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}])
        else:
            book = find_book(point)
            serializer.save(user=self.request.user, book=book, point=point)

    def list(self, request):
        user = request.user
        my_bookmarks = user.bookmark_set.order_by('id')
        serializer = BookmarkSerializer(my_bookmarks, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        bookmark = self.get_object()
        bookmark.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

