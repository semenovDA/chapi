from django_filters import rest_framework as filters
from .models import Account

class AccountFilter(filters.FilterSet):
    firstName = filters.CharFilter(lookup_expr='icontains')
    lastName = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Account
        fields = [
            'firstName', 
            'lastName', 
            'email'
        ]
