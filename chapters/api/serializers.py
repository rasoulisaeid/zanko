from rest_framework import serializers
from points.api.serializers import PointSerializer
from chapters.models import Chapter
from rest_framework.response import Response
from books.models import Book

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    # points = PointSerializer(many=True, read_only=True)
    name = serializers.CharField()
    data = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'book', 'user', 'data')
   
    