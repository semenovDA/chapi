from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exceptions import *
from .utils import ValidateDict

import logging
logger = logging.getLogger(__name__)

class CustomPermission(BasePermission):

    def valid_request(self, request):
        kwargs = request.resolver_match.kwargs

        for k in kwargs:
            if(int(kwargs[k]) <= 0):
                msg = '{} should not be null or negitive int'.format(k)
                raise BadRequestException(msg)

        if not ValidateDict(request.data):
            raise BadRequestException('Invalid request body')
            
    def has_permission(self, request, view):
        self.valid_request(request)
        return request.user.is_authenticated or request.method in SAFE_METHODS 
        