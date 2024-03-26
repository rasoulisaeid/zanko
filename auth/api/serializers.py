from rest_framework import serializers
from auth.models import User
from rest_framework.decorators import action

class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    staff = serializers.BooleanField(read_only=True)
    introduction = serializers.CharField()
    balance = serializers.IntegerField()
    class Meta:
        model = User
        fields = ('id', 'name','balance', 'phone', 'introduction', 'staff')
        




    
