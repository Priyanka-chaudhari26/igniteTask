from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    location_type = serializers.JSONField()  
    employement_type = serializers.JSONField()  
    skills = serializers.JSONField()

    class Meta:
        model = Job
        fields = '__all__'

    def create(self, validated_data):
        
        job = Job.objects.create(**validated_data)
        return job