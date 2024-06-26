from unicodedata import name
from tags.models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from zanko.permissions import JustOwner
from auth.models import User
from points.models import Point, TagPoint
from purchases.models import Purchase
from studies.models import Study
from bookmarks.models import Bookmark
from points.api.serializers import PointSerializer
import jdatetime as time
import pytz

def study_order():
    time.set_locale("fa_IR")
    timezone = pytz.timezone('Asia/Tehran')
    date = time.datetime.now(timezone)
    order = str(date)[0:19]
    order += ("+" + str(date + time.timedelta(minutes=1))[0:19])
    return order

# class OwnerOnly(BasePermission):
#   def has_permission(self, request, object):
#       return request.user == object.user()

class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def create(self, request):
        tag = Tag.objects.filter(name=self.request.data.get('name'), user=self.request.user)
        if tag:
            return Response(data=[{'status': status.HTTP_200_OK, "message":'existed'}])
        else:
            Tag.objects.create(name=request.data.get('name'), user=request.user)
            return Response(data=[{'status': status.HTTP_200_OK, "message":'created'}])

    def list(self, request):
        user = request.user
        # Each book has many chapters and we load them
        # my_books = user.book_set.prefetch_related('chapters').order_by('id')
        if user.staff:
            user_tags = user.tag_set.order_by('id')
            serializer = TagSerializer(user_tags, many=True)
            return Response(serializer.data)
        else:
            all_tags = Tag.objects.all()
            allowed_tags = []
            for tag in all_tags:
                tag_points = tag.point_set.all()
                for point in tag_points:
                    chapter = point.chapter
                    book = chapter.book
                    book_purchased = Purchase.objects.filter(book=book, user=user) 
                    if book_purchased and tag not in allowed_tags:
                        allowed_tags.append(tag)
            serializer = TagSerializer(allowed_tags, many=True)
            return Response(serializer.data)            

        

    def destroy(self, request, *args, **kwargs):
        tag = self.get_object()
        tag.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        tag = self.get_object()
        prev_tag = Tag.objects.filter(name=request.data.get('name'), user=request.user)
        if prev_tag:
            return Response({'status': status.HTTP_200_OK, "message":'existed'})
        else:
            tag.name = request.data.get('name')
            tag.save()
            return Response({'status': status.HTTP_200_OK, "message":'updated'})     
        

    @action(detail=True, methods=['POST'])
    def set_tag(self, request, *args, **kwargs):
        tag = self.get_object()
        point = Point.objects.get(id=request.data.get('point'))
        tag_point = TagPoint.objects.filter(tag=tag, point=point)
        if not tag_point:
            TagPoint.objects.create(tag=tag, point=point)
        else:
            tag_point.delete()    
        return Response({'status': status.HTTP_200_OK, "message":'done'})    

    @action(detail=True, methods=['GET'])
    def points(self, request, *args, **kwargs):
        user = request.user
        tag_name = self.get_object().name
        tags = Tag.objects.filter(name=tag_name)
        points = self.get_object().point_set.all()
        allowed_points = []
        if not user.staff:
            for tag in tags:
                points = tag.point_set.all()
                for point in points:
                    chapter = point.chapter
                    book = chapter.book
                    book_purchased = Purchase.objects.filter(book=book, user=user) 
                    if not book_purchased:
                        continue
                    point.info = chapter.name + "_" + book.name
                    # Add study
                    study = Study.objects.filter(point=point, user=request.user)
                    if study:
                        next_time = study[0].order.split("+")[-1]
                        study[0].ready = time.datetime.strptime(next_time, "%Y-%m-%d %H:%M:%S") < time.datetime.now(pytz.timezone('Asia/Tehran'))
                        point.study = study
                    else:
                        point.study = [Study.objects.create(user=request.user, point=point, order=study_order())]

                    # Add bookmark    
                    bookmark = Bookmark.objects.filter(point=point, user=request.user).first()
                    if bookmark:
                        point.bookmark = True
                    allowed_points.append(point)  
            serializer = PointSerializer(allowed_points, many=True)
            return Response(serializer.data)          
        else:
            points = self.get_object().point_set.all()
            for point in points:
                chapter = point.chapter
                book = chapter.book
                point.info = chapter.name + "_" + book.name
                    # Add study
                study = Study.objects.filter(point=point, user=request.user)
                if study:
                    next_time = study[0].order.split("+")[-1]
                    study[0].ready = time.datetime.strptime(next_time, "%Y-%m-%d %H:%M:%S") < time.datetime.now(pytz.timezone('Asia/Tehran'))
                    point.study = study
                else:
                    point.study = [Study.objects.create(user=request.user, point=point, order=study_order())]

                # Add bookmark    
                bookmark = Bookmark.objects.filter(point=point, user=request.user).first()
                if bookmark:
                    point.bookmark = True
            serializer = PointSerializer(points, many=True,)
            return Response(serializer.data)
