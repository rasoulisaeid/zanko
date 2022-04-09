from rest_framework import serializers
from bookmarks.models import Bookmark
from auth.models import User
from rest_framework.decorators import action

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    point = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ('id', 'book', 'user', 'point')
        




    
