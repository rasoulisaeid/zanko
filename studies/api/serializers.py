from rest_framework import serializers
from studies.models import Study

class StudySerializer(serializers.HyperlinkedModelSerializer):
    point = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    level = serializers.CharField()
    order = serializers.CharField()
    function = serializers.CharField()
    ready = serializers.BooleanField(default=False)

    class Meta:
        model = Study
        fields = ('id', 'point', 'user', 'level', 'order', 'function', 'ready')
        
    




    
