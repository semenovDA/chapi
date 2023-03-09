from rest_framework.response import Response
from rest_framework import generics, status

from .models import AnimalLocation
from .serializers import AnimalLocationSerializer
from .filters import AnimalLocationFilter

from animal.models import Animal

from location.models import Location

from core.exceptions import *
from core.utils import validate_dict_number
from core.permissions import CustomPermission

from django_filters import rest_framework as filters

# POST on http://localhost:8000/animals/{animalId}/locations/{pointId}
class AnimalLocationAddition(generics.RetrieveAPIView):
    queryset = AnimalLocation.objects.all()
    serializer_class = AnimalLocationSerializer
    http_method_names = ['post', 'delete']
    permission_classes = (CustomPermission,)

    def post(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId"))
        pointId = int(kwargs.get("pointId"))

        try:
            animal = Animal.objects.get(pk=animalId)
            location = Location.objects.get(pk = pointId)

        except Exception as e:
            raise NotFoundException(e.args)

        if animal.lifeStatus == 'DEAD':
            raise BadRequestException('animal lifeStatus is DEAD')

        if animal.chippingLocationId == location and animal.visitedLocations.count() == 0:
            raise BadRequestException('animal didnt moved from chippingLocationId')

        if animal.visitedLocations.count():
            if animal.visitedLocations.last().locationPointId == location:
                raise BadRequestException('animal didnt moved from the last visited point')

        animal_location = AnimalLocation.objects.create(locationPointId = location)
        animal.visitedLocations.add(animal_location)
        animal.save()

        serializer = AnimalLocationSerializer(animal_location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        pointId = int(kwargs.get("pointId", 0))

        try:
            animal = Animal.objects.get(pk=animalId)

            if not animal.visitedLocations.filter(pk=pointId).exists():
                raise NotFoundException('pointId not exists in visitedLocations')
                
        except Exception as e:
            raise NotFoundException(e.args)

        animal.visitedLocations.remove(pointId)

        if animal.visitedLocations.count():
            if animal.chippingLocationId == animal.visitedLocations.first().locationPointId:
                animal.visitedLocations.remove(animal.visitedLocations.first())
        
        return Response({})

'''
GET on http://localhost:8000/animals/{animalId}/locations
Additional parmaetrs: startDateTime, endDateTime, from, size
'''
class AnimalLocationList(generics.ListAPIView):
    queryset = AnimalLocation.objects.all().order_by('id')
    serializer_class = AnimalLocationSerializer
    http_method_names = ['get', 'put']
    permission_classes = (CustomPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnimalLocationFilter

    def get(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId"))
        animal = Animal.objects.get(pk = animalId)
        self.queryset = self.queryset.filter(
            id__in = animal.visitedLocations.all()
        )
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        
        if not validate_dict_number(request.data):
            raise BadRequestException('Invalid request body')

        try:
            animal = Animal.objects.get(pk=animalId)
            location = Location.objects.get(pk = request.data['locationPointId'])

            if not animal.visitedLocations.filter(
                pk=request.data['visitedLocationPointId']
            ).exists():

                raise NotFoundException('There not visitedLocationPointId in animal.visitedLocations')

        except Exception as e:
            raise NotFoundException(e.args)

        animal_location = animal.visitedLocations.get(pk=request.data['visitedLocationPointId'])

        if animal_location.locationPointId == location:
            raise BadRequestException('locationPointId equels location')

        if animal_location.locationPointId == animal.visitedLocations.first().locationPointId:
            if animal.chippingLocationId == location:
                raise BadRequestException('locationPointId cannot be replaced to chippingLocationId') 

        for i in range(1, animal.visitedLocations.count() - 1):

            next_, cur_, prev_ = animal.visitedLocations.all()[i-1:i+2]

            # next element check
            if next_.locationPointId == location and cur_ == animal_location:
                raise BadRequestException('This visit location matches the next')

            # previous element check
            if prev_.locationPointId == location and cur_ == animal_location:
                raise BadRequestException('This visit location matches the previous')

        animal_location.locationPointId = location
        animal_location.save()

        serializer = AnimalLocationSerializer(animal_location)
        return Response(serializer.data)    