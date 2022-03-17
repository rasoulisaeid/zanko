from rest_framework import serializers, status
from rest_framework.response import Response
from subjects.models import Subject
from auth.models import User
from rest_framework.decorators import action

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    chapter = serializers.PrimaryKeyRelatedField(read_only=True)
    # chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name')
        
    




    
