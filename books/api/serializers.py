from rest_framework import serializers, status
from rest_framework.response import Response
from books.models import Book
from auth.models import User

class BookSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'description','user')
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        book = Book.objects.create(**validated_data)
        return book 



    
