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
from points.api.serializers import PointSerializer

# class OwnerOnly(BasePermission):
#   def has_permission(self, request, object):
#       return request.user == object.user()

class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        user = request.user
        # Each book has many chapters and we load them
        # my_books = user.book_set.prefetch_related('chapters').order_by('id')
        user_tags = user.tag_set.order_by('id')
        serializer = TagSerializer(user_tags, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        tag = self.get_object()
        tag.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        tag = self.get_object()
        tag.name = request.data.get('name')
        tag.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})

    @action(detail=True, methods=['GET'])
    def points(self, request, *args, **kwargs):
        points = self.get_object().point_set.all()
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)