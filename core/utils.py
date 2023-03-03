from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from .exceptions import *

import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if(type(exc) == NotAuthenticated): # Overriding default 500 to 401 HTTP status 

        return exception_handler(
            AuthenticationException('Request from unauthorized account'),
            None
        )

    return response

def validate_dict_array(data):
    for v in data.values():
        if v == None:
            return False
        if type(v) == list:
            for i in v:
                if i == None:
                    return False
                if i <= 0:
                    return False  
    return True

def validate_dict_string(data):
    for v in data.values():
        if type(v) == str:
            if v == '':
                return False
    return True

def validate_dict_number(data):
    for v in data.values():
        if(v == None):
            return False
        if type(v) == int and int(v) <= 0:
            return False
    return True

def ValidateDict(data):
    return validate_dict_string(data) \
        and validate_dict_array(data)