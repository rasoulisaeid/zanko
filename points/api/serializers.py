from rest_framework import serializers, status
from rest_framework.response import Response
from points.models import Point
from auth.models import User
from rest_framework.decorators import action

class PointSerializer(serializers.HyperlinkedModelSerializer):
    chapter = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    explains = serializers.CharField(style={'base_template': 'textarea.html'})
    importants = serializers.CharField(style={'base_template': 'textarea.html'})
    regulars = serializers.CharField(style={'base_template': 'textarea.html'})
    reminders = serializers.CharField(style={'base_template': 'textarea.html'})
    attentions = serializers.CharField(style={'base_template': 'textarea.html'})
    questions = serializers.CharField(style={'base_template': 'textarea.html'})
    image = serializers.FileField()
    voice = serializers.FileField()
    rtl = serializers.BooleanField(default=True)
    # chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Point
        fields = ('id', 'user', 'chapter', 'explains', 'importants', 'regulars',
        'reminders', 'questions', 'attentions', 'image', 'voice','rtl')
        
    




    
