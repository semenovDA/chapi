from rest_framework.response import Response
from rest_framework import generics
from .models import Location
from animal.models import Animal
from animal_location.models import AnimalLocation

from .serializers import LocationSerializer
from core.exceptions import *

import logging
logger = logging.getLogger(__name__)

from core.permissions import CustomPermission

# POST on http://localhost:8000/locations
class CreateLocation(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (CustomPermission,)
    
# GET, PUT, DELETE on http://localhost:8000/locations/{pointId}
class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (CustomPermission,)

    # TODO: Optimize
    def delete(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0)) 
        
        animal_locations = list(
            AnimalLocation.objects.filter(locationPointId=pk).values_list('id', flat=True)
        )

        if(Animal.objects.filter(visitedLocations__in = animal_locations)):
            raise BadRequestException('Location is used by animal')

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)  