from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, AccountSerializer
from .models import Account

from core.exceptions import *
from core.permissions import CustomPermission

import logging
logger = logging.getLogger(__name__)

# Register API
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
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
    
        # Define all query_params
        firstName = self.request.query_params.get("firstName", '') 
        lastName = self.request.query_params.get("lastName", '') 
        email = self.request.query_params.get("email", '') 
        from_ = self.request.query_params.get('from', '0')
        size = self.request.query_params.get('size', '10')

        if(not (from_.isnumeric() and size.isnumeric())):
            raise BadRequestException('from or size is not numeric')

        from_, size = int(from_), int(size)

        if(from_ < 0 or size <= 0):
            raise BadRequestException('from and size should be > 0 and not equals null')

        # Filter by query_params
        queryset = Account.objects.filter(firstName__icontains = firstName,
                                    lastName__icontains = lastName,
                                    email__icontains = email).order_by('-id').reverse()

        return queryset[from_:from_+size]


# GET, PUT, DELETE on http://localhost:8000/accounts/{accountId}
class AccountDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (CustomPermission,)

    def put(self, request, *args, **kwargs):

        # Проверка попытки изменении не своего аккаунта
        if(int(request.user.id) != int(kwargs.get("pk"))):
            raise ForbiddenException('Обновление не своего аккаунта')

        return self.update(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        serializer = RegisterSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # set password by method set_password if password changed
        if('password' in request.data):
            request.user.set_password(request.data['password'])
            request.user.save()
            
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):

        if int(kwargs.get("pk")) != request.user.id:
            raise ForbiddenException('Удаление не своего аккаунта')
        
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)