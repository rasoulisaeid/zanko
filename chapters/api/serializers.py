from rest_framework import serializers
from chapters.models import Chapter

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'get_book')