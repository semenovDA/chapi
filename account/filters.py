from django_filters import rest_framework as filters
from .models import Account
from core.exceptions import BadRequestException

class AccountFilter(filters.FilterSet):

    class Meta:
        model = Account
        fields = [
            'firstName', 
            'lastName', 
            'email'
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