from rest_framework import serializers, status
from rest_framework.response import Response
from books.api.serializers import BookSerializer
from categories.models import Category
from auth.models import User
from rest_framework.decorators import action

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'user')
        




    
