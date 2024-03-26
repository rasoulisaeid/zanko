from .serializers import UserSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from zanko.permissions import JustOwner
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

def balance_points(code):
    if code == "buy_points_200":
        return 200
    elif code == "buy_points_100":
        return 100
    else:
        return 50        

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def update(self, request, *args, **kwargs):
        user = request.user
        if request.data.get('pay') == "yes":
            user.balance += balance_points(request.data.get('balance'))
        else:
            user.name = request.data.get('name')
            user.introduction = request.data.get('info')
        user.save()
        return Response({'status': status.HTTP_200_OK, "update":'yes'})

    
    def list(self, request,  *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    

