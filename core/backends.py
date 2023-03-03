from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from account.models import Account
from .exceptions import *
import base64

class Authentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth_header or auth_header[0].lower() != 'basic':
            return (AnonymousUser, None)

        if(len(auth_header) == 1 or len(auth_header) > 2):
            return (AnonymousUser, None)

        decoded_credentials = base64.b64decode(auth_header[1]).decode("utf-8").split(':')
        email, password = decoded_credentials[0], decoded_credentials[1]

        try:
            user = Account.objects.get(email=email)
            if(user.check_password(password)):
                return (user, None)
            raise AuthenticationException('Incorrect creditals')

        except Account.DoesNotExist:
            raise AuthenticationException('Incorrect creditals')