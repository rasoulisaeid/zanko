from favorites.models import Favorite
from .serializers import FavoriteSerializer
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

class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        user = request.user
        my_favorites = user.favorite_set.order_by('id')
        serializer = FavoriteSerializer(my_favorites, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        favorite = self.get_object()
        favorite.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        favorite = self.get_object()
        favorite.name = request.data.get('name')
        favorite.description = request.data.get('description')
        favorite.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})
