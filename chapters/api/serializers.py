from rest_framework import serializers
from subjects.api.serializers import SubjectSerializer
from chapters.models import Chapter
from rest_framework.response import Response
from books.models import Book

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    name = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'book', 'user', 'subjects')
   
    