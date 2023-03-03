from rest_framework import status
from rest_framework.exceptions import APIException

class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class BadRequestException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class NotFoundException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class ConflictExistsException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_409_CONFLICT)


class AuthenticationException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)

        
class ForbiddenException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)