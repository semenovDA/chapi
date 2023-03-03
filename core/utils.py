from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from account.models import Account
from .exceptions import *

import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if(type(exc) == NotAuthenticated):

        return exception_handler(
            AuthenticationException('Request from unauthorized account'),
            None
        )

    return response

def ValidateDict(data):
    for v in data.values():

        if(v == None):
            return False

        if(type(v) != list and type(v) != str):
            if(v <= 0):
                return False

        elif(type(v) == list):
            for i in v:
                if(i == None):
                    return False
                if(i <= 0):
                    return False        
        
        elif(type(v) == str):
            if v == '':
                return False

    return True