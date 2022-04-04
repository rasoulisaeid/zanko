from rest_framework import serializers
from favorites.models import Favorite
from auth.models import User
from rest_framework.decorators import action

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'user')
        




    
