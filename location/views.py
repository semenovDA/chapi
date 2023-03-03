from rest_framework.response import Response
from rest_framework import generics
from .models import Location
from animal.models import Animal
from animal_location.models import AnimalLocation

from .serializers import LocationSerializer
from core.exceptions import *

import logging
logger = logging.getLogger(__name__)

from rest_framework.permissions import IsAuthenticatedOrReadOnly

# POST on http://localhost:8000/locations
class CreateLocation(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def post(self, request, *args, **kwargs):
        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Request from unauthorized account')

        return self.create(request, *args, **kwargs)

# GET, PUT, DELETE on http://localhost:8000/locations/{pointId}
class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        pk = int(self.kwargs.get("pk", 0))

        if(pk <= 0):
            raise BadRequestException('locationId should not be null or negitive int')

        try:
            location = Location.objects.get(pk=pk)

            for permission in self.get_permissions():
                if permission.has_permission(self.request, self):
                    logger.error(bool(self.request.user.is_authenticated))

            # logger.error(self.check_object_permissions(self.request, location))

            return location

        except Exception as e:
            raise NotFoundException(e.args)
            
    def put(self, request, *args, **kwargs):

        if(int(kwargs.get("pk", 0)) <= 0): # проверка на правильность параметров
            raise BadRequestException('locationId should not be negitive or null')

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        instance = self.get_object()

        pk = int(kwargs.get("pk", 0)) 

        if(pk <= 0): # проверка на правильность параметров
            raise BadRequestException('accountId should not be negitive or null')

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Request from unauthorized account')
        
        animal_locations = list(
            AnimalLocation.objects.filter(locationPointId=pk).values_list('id', flat=True)
        )

        if(
            Animal.objects.filter(chippingLocationId=pk).exists() or
            Animal.objects.filter(visitedLocations__in = animal_locations)  
        ):
            raise BadRequestException('Location is used by animal')

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)  