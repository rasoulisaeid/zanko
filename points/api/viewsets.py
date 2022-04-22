from chapters.models import Chapter
from points.models import Point
from studies.models import Study
from bookmarks.models import Bookmark
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from zanko.permissions import JustOwner
from .serializers import PointSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import jdatetime as time
import pytz

def study_order():
    time.set_locale("fa_IR")
    timezone = pytz.timezone('Asia/Tehran')
    date = time.datetime.now(timezone)
    order = str(date)[0:19]
    order += ("+" + str(date + time.timedelta(minutes=1))[0:19])
    return order

class PointViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner, IsAuthenticated]
    queryset = Point.objects.all()
    serializer_class = PointSerializer


    def perform_create(self, serializer):
        chapter = Chapter.objects.get(id=self.request.data.get('chapter'))
        serializer.save(user=self.request.user, chapter=chapter)


    def list(self, request):
        # Note that we can't use request.data
        chapter_id = request.query_params.get('chapter', None)
        chapter = Chapter.objects.get(pk=chapter_id)
        points = chapter.points.order_by('id')
        for point in points:
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
                
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        point = self.get_object()
        point.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        point = self.get_object()
        point.text = request.data.get('text')
        point.title = request.data.get('title')
        attachments = request.data.get('attachments')
        image_old = attachments.split('_')[0]
        voice_old = attachments.split('_')[1]
        
        if image_old != "yes":
            point.image = request.data.get('image')
        if voice_old != "yes":
            point.voice = request.data.get('voice')
        
        point.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})

