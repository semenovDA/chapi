from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.exceptions import *

from .models import AnimalType

class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalType
        fields = "__all__"

    def validate(self, attrs):
        type = attrs['type']
        if(AnimalType.objects.filter(type=type).exists()):
            raise ConflictExistsException('AnimalType is not unique value')
        return attrs