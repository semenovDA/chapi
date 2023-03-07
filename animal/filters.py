from django_filters import rest_framework as filters
from .models import Animal
from core.exceptions import BadRequestException
from core.utils import validate_dict_number
import logging
logger = logging.getLogger(__name__)

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