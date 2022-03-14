from rest_framework import serializers
from rest_framework.response import Response
from books.models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Book
        fields = ('id', 'name', 'description',)
        
    def create(self, validated_data):
        book = Book.objects.create(**validated_data)

        return book



    
