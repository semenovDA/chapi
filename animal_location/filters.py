from django_filters import rest_framework as filters
from .models import AnimalLocation

class AnimalLocationFilter(filters.FilterSet):
    
    startDateTime = filters.IsoDateTimeFilter(
        field_name='dateTimeOfVisitLocationPoint', lookup_expr='gte')

    endDateTime = filters.IsoDateTimeFilter(
        field_name='dateTimeOfVisitLocationPoint', lookup_expr='lte')

    class Meta:
        model = AnimalLocation
        fields = ['dateTimeOfVisitLocationPoint']