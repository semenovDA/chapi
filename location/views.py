from rest_framework.response import Response
from rest_framework import generics, status

from .models import Location
from .serializers import LocationSerializer

from animal.models import Animal
from animal_location.models import AnimalLocation

from core.exceptions import BadRequestException
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


    def delete(self, request, *args, **kwargs):

        animal_locations = list(
            AnimalLocation.objects
            .filter(locationPointId=int(kwargs.get("pk")))
            .values_list('id', flat=True)
        )

        if(Animal.objects.filter(visitedLocations__in = animal_locations)):
            raise BadRequestException('Location is used by animal visitedLocations')

        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)  