from rest_framework import serializers
from core.exceptions import *

from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

    def validate(self, data):
        if(data['latitude'] < -90 or data['latitude'] > 90):
            raise BadRequestException("Latitude should be in range between -90 and 90")
        if(data['longitude'] < -180 or data['longitude'] > 180):
            raise BadRequestException("Longitude should be in range between -180 and 180")
        return data
