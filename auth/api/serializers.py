from rest_framework import serializers
from auth.models import User
from rest_framework.decorators import action

class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    introduction = serializers.CharField()
    class Meta:
        model = User
        fields = ('id', 'name','balance', 'phone', 'introduction')
        




    
