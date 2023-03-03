from rest_framework import serializers

from .models import Animal
from core.exceptions import *

from animal_type.models import AnimalType
from animal_location.models import AnimalLocation 
from location.models import Location
from account.models import Account


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"

    
    def validate(self, attrs):
        # TODO: Maybe validate at the model part
        if(attrs['weight'] <= 0 or attrs['length'] <= 0 or attrs['height'] <= 0):
            raise BadRequestException('Validation Error')
        return attrs
