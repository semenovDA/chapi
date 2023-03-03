from rest_framework import serializers

from .models import AnimalLocation

class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = "__all__"