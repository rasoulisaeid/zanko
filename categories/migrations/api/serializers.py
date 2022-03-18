from rest_framework import serializers, status
from rest_framework.response import Response
from chapters.api.serializers import ChapterSerializer
from books.models import Book
from auth.models import User
from rest_framework.decorators import action

class BookSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'description','user', 'chapters')
        




    
