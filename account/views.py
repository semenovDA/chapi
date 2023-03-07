from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .serializers import RegisterSerializer, AccountSerializer
from .models import Account
from .filters import AccountFilter

from core.exceptions import *
from core.permissions import OwnerPermission

"""
POST on http://localhost:8000/registration
Request body:
{
    firstName: String
    lastName: String
    email: Email(String)
    password: String
}
Respone: 200 | 400 | 403 | 409 
"""
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        if(self.request.user.is_authenticated == True):
            raise ForbiddenException('You are already logged in')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
GET on http://localhost:8000/accounts/search
Additional parmaetrs: firstname, lastName, email, from, size
"""
class AccountList(generics.ListAPIView):
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AccountFilter


# GET, PUT, DELETE on http://localhost:8000/accounts/{accountId}
class AccountDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (OwnerPermission,)

    def update(self, request, *args, **kwargs):
        serializer = RegisterSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # set password by method set_password if password changed
        if('password' in request.data):
            request.user.set_password(request.data['password']) # pbkdf2_sha256 hashed
            request.user.save()
            
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)