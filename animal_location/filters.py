from django_filters import rest_framework as filters
from .models import AnimalLocation
from core.exceptions import BadRequestException

class AnimalLocationFilter(filters.FilterSet):
    startDateTime = filters.IsoDateTimeFilter(field_name='dateTimeOfVisitLocationPoint', lookup_expr='gte')
    endDateTime = filters.IsoDateTimeFilter(field_name='dateTimeOfVisitLocationPoint', lookup_expr='lte')


    class Meta:
        model = AnimalLocation
        fields = ['dateTimeOfVisitLocationPoint']

    def filter_queryset(self, queryset):
        try:
            from_ = int(self.request.query_params.get('from', '0'))
            size = int(self.request.query_params.get('size', '10'))
        except:
            raise BadRequestException('Invaild query parameters')

        if(from_ < 0 or size <= 0):
            raise BadRequestException('from and size should be > 0 and not equals null')

        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)

        return queryset[from_:from_+size]