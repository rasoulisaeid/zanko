from rest_framework import serializers, status
from rest_framework.response import Response
from tags.models import Tag
from auth.models import User
from rest_framework.decorators import action

class TagSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'user')
        
    def get_points(self):
        return self.point_set.all()
        




    
