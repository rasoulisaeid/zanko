from rest_framework import serializers, status
from rest_framework.response import Response
from chapters.api.serializers import ChapterSerializer
from books.models import Book
from auth.models import User
from rest_framework.decorators import action

class BookSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    data = serializers.CharField(read_only=True)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    category = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    sample = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
    purchased = serializers.BooleanField(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'name', 'description', 'user', 'data', 'category', 'sample', 'price', 'purchased')
        




    
