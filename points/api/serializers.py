from rest_framework import serializers, status
from rest_framework.response import Response
from points.models import Point
from auth.models import User
from rest_framework.decorators import action

class PointSerializer(serializers.HyperlinkedModelSerializer):
    chapter = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField()
    title = serializers.CharField(style={'base_template': 'textarea.html'})
    text = serializers.CharField(style={'base_template': 'textarea.html'})
    image = serializers.FileField(required=False)
    voice = serializers.FileField(required=False)
    bookmark = serializers.CharField(default="no_0")
    # chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Point
        fields = ('id', 'user', 'chapter', 'type', 'title', 'text','image', 'voice', 'bookmark')
        
    




    
