from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exceptions import *

class CustomPermission(BasePermission):

    def has_permission(self, request, view):

        kwargs = request.resolver_match.kwargs

        # Checking request
        pk = int(kwargs.get('pk', 0))

        if(pk <= 0 and 'pk' in kwargs):
            raise BadRequestException('pk should not be null or negitive int')

        return request.user.is_authenticated or request.method in SAFE_METHODS 
        