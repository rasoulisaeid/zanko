from rest_framework import serializers
from purchases.models import Purchase

class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    description = serializers.CharField()
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.CharField()

    class Meta:
        model = Purchase
        fields = ('id', 'description', 'user', 'book', 'price')
        




    
