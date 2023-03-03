from rest_framework import serializers
from .models import Account

from django.core.exceptions import ValidationError
from core.exceptions import *

# Account Serializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'firstName', 'lastName', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'firstName', 'lastName', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'firstName': {'required': True},
            'lastName': {'required': True}
        }

    def to_internal_value(self, data):
        data = self.validate(data)
        return super(RegisterSerializer, self).to_internal_value(data)

    def validate(self, attrs):
        data = dict(attrs)
        email = data.pop('email', None)
        
        for v in list(data.values()):
            if (v == '' or v == None):
                raise BadRequestException('Validation Error')

        # TODO: need optimization
        if(self.instance != None):
            if(Account.objects.filter(email=email).exists() and self.instance.email != email):
                raise ConflictExistsException('Not a unique value')
        else:
            if(Account.objects.filter(email=email).exists()):
                raise ConflictExistsException('Not a unique value')
        return attrs

    def create(self, validated_data):
        account = Account.objects.create_user(
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            email = validated_data['email']
        )
        account.set_password(validated_data['password'])
        account.save()
        return account
    