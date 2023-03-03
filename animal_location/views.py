from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status

from .models import AnimalLocation
from .serializers import AnimalLocationSerializer

from animal.models import Animal
from animal.serializers import AnimalSerializer

from location.models import Location

from core.exceptions import *
from core.utils import ValidateDict

import logging
logger = logging.getLogger('django')

# POST on http://localhost:8000/animals/{animalId}/locations/{pointId}
class AnimalLocationAddition(generics.RetrieveAPIView):
    queryset = AnimalLocation.objects.all()
    serializer_class = AnimalLocationSerializer
    http_method_names = ['post', 'delete']

    def post(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        pointId = int(kwargs.get("pointId", 0))

        if(self.request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if animalId <= 0 or pointId <= 0:
            raise BadRequestException('animalId or pointId cannot be null or negitive')

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

        if(self.request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if animalId <= 0 or pointId <= 0:
            raise BadRequestException('animalId or pointId cannot be null or negitive')

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
    queryset = AnimalLocation.objects.all()
    serializer_class = AnimalLocationSerializer
    http_method_names = ['get', 'put']

    def get(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        
        if(animalId <= 0):
            raise BadRequestException('animalId should not be null or negitive')
            
        try:
            animal = Animal.objects.get(pk=animalId)
        except Animal.DoesNotExist:
            raise NotFoundException('Animal type not found')

        # Define all query_params
        startDateTime = self.request.query_params.get('startDateTime', None) 
        endDateTime = self.request.query_params.get('endDateTime', '') 
        from_ = self.request.query_params.get('from', '0')
        size = self.request.query_params.get('size', '10')
            
        if(not (from_.isnumeric() and size.isnumeric())):
            raise BadRequestException('from or size is not numeric')

        from_, size = int(from_), int(size)

        if(from_ < 0 or size <= 0):
            raise BadRequestException('from and size should be > 0 and not equals null')

        filter = {}
        if startDateTime != None and endDateTime != None:
            filter['dateTimeOfVisitLocationPoint__range'] = (startDateTime, endDateTime)

        queryset = animal.visitedLocations.filter(**filter)
        serializer = AnimalLocationSerializer(queryset, many=True)
        return Response(serializer.data[from_:from_+size])



    def put(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        
        if(self.request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')
        
        if(animalId <= 0):
            raise BadRequestException('animalId cannot be null or negitive')

        if not ValidateDict(request.data):
            raise BadRequestException('Unvaild request body')

        try:
            animal = Animal.objects.get(pk=animalId)
            location = Location.objects.get(pk = request.data['locationPointId'])

            if not animal.visitedLocations.filter(pk=request.data['visitedLocationPointId']).exists():
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