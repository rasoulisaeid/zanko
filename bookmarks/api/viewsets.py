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
from studies.models import Study
from auth.models import User
from points.api.serializers import PointSerializer
import jdatetime as time
import pytz

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

    

    def destroy(self, request, *args, **kwargs):
        bookmark = self.get_object()
        bookmark.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 


    def list(self, request, *args, **kwargs):
        points = Point.objects.all()
        bookmark_id_list = []
        for point in list(points):
            chapter = point.chapter
            book = chapter.book
            point.info = chapter.name + "_" + book.name
            bookmark = Bookmark.objects.filter(point=point, user=request.user)
            print("user-phone: " + str(request.user.phone) + "\n" + "point-id: " + str(point.id))
            if bookmark:
                point.bookmark = True
                # Add study
                study = Study.objects.filter(point=point, user=request.user)
                next_time = study[0].order.split("+")[-1]
                study[0].ready = time.datetime.strptime(next_time, "%Y-%m-%d %H:%M:%S") < time.datetime.now(pytz.timezone('Asia/Tehran'))
                point.study = study 
                print("yes")
                bookmark_id_list.append(point)
                     
            # Add bookmark    
        # bookmark_points = Point.objects.filter(id__in=bookmark_id_list)    
        serializer = PointSerializer(bookmark_id_list, many=True)
        return Response(serializer.data)
   

    

