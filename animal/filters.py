from django_filters import rest_framework as filters
from .models import Animal

class AnimalFilter(filters.FilterSet):
    startDateTime = filters.IsoDateTimeFilter(field_name='chippingDateTime', lookup_expr='gte')
    endDateTime = filters.IsoDateTimeFilter(field_name='chippingDateTime', lookup_expr='lte')

    class Meta:
        model = Animal
        fields = [
            'chippingDateTime', 
            'chipperId', 
            'chippingLocationId', 
            'lifeStatus', 
            'gender'
        ]