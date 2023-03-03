from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from .models import Animal
from .serializers import AnimalSerializer
from core.exceptions import *
from core.utils import ValidateDict

from animal_type.models import AnimalType
from animal_location.models import AnimalLocation 
from location.models import Location
from account.models import Account

import datetime

# POST on http://localhost:8000/animals
class CreateAnimal(generics.CreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def post(self, request, *args, **kwargs):

        if(self.request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if not ValidateDict(request.data):
            raise BadRequestException('Invalid values')
        
        try:
            animalTypes = request.data['animalTypes']
            Account.objects.get(pk=request.data['chipperId'])
            Location.objects.get(pk=request.data['chippingLocationId'])

            if(len(list(set(animalTypes))) != len(animalTypes)):
                raise ConflictExistsException('animalTypes has duplicates')

            if AnimalType.objects.filter(id__in=animalTypes).count() != len(animalTypes):
                raise NotFoundException('animalTypes not found')
        
        except Exception as e:

            if(type(e) == Account.DoesNotExist):
                raise NotFoundException('Account not found')

            if(type(e) == Location.DoesNotExist):
                raise NotFoundException('Location not found')

            raise e


        return self.create(request, *args, **kwargs)

# GET, PUT, DELETE on http://localhost:8000/animals/{animalId}
class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    http_method_names = ['get', 'put', 'delete']
    # TODO: raise exception on DELETE if AnimalType related with Animal

    def get(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0))

        if(pk <= 0):
            raise BadRequestException('animalId should not be null or negitive')

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0))

        if(pk <= 0):
            raise BadRequestException('animalId should not be null or negitive')

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if not ValidateDict(request.data):
            raise BadRequestException('Invalid values')

        try:
            Account.objects.get(pk=request.data['chipperId'])
            Location.objects.get(pk=request.data['chippingLocationId'])

        except Exception as e:
            # TODO: check if type(e) in [err, err, err] raise NotFound with object not found

            if(type(e) == Account.DoesNotExist):
                raise NotFoundException('Account not found')

            if(type(e) == Location.DoesNotExist):
                raise NotFoundException('Location not found')

            raise e

        instance = self.get_object()

        # LIFE STATUS HANDLING 
        if('lifeStatus' in request.data): # TODO: replace in db action

            if(request.data['lifeStatus'] == 'DEAD'):
                instance.deathDateTime = datetime.datetime.now().isoformat()
                instance.save()

            elif(instance.lifeStatus == 'DEAD' and request.data['lifeStatus'] == 'ALIVE'):
                raise BadRequestException('Cannot change DEAD status on ALIVE')

        # CHIPPING LOCATION HANDLING
        if(instance.visitedLocations.count() > 0):
            if(instance.visitedLocations.first().locationPointId.id == request.data['chippingLocationId']):
                raise BadRequestException('chippingLocationId should not be a first visitedLocation point')

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0))
        if(pk <= 0):
            raise BadRequestException('AnimalId should not be negitive or null')
        
        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        try:
            animal = Animal.objects.get(pk=pk)
            if(animal.visitedLocations.count() != 0):
                raise BadRequestException('Animal has visitLocations')

        except Animal.DoesNotExist:
            raise NotFoundException('animalId not found')

        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK) 

"""
GET on http://localhost:8000/animals/search
Additional parmaetrs: firstname, lastName, email, from, size
"""
class AnimalList(generics.ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        
        # Define all query_params
        startDateTime = self.request.query_params.get('startDateTime', None) 
        endDateTime = self.request.query_params.get('endDateTime', None) 
        chipperId = self.request.query_params.get('chipperId', None) 
        chippingLocationId = self.request.query_params.get('chippingLocationId', None)
        lifeStatus = self.request.query_params.get('lifeStatus', None)
        gender = self.request.query_params.get('gender', None)
        from_ = self.request.query_params.get('from', '0')
        size = self.request.query_params.get('size', '10')

        if(not (from_.isnumeric() and size.isnumeric())):
            raise BadRequestException('from or size is not numeric')

        from_, size = int(from_), int(size)

        if(from_ < 0 or size <= 0):
            raise BadRequestException('from and size should be > 0 and not equals null')

        '''
            TODO: Optimize if statments
            START
        '''

        filter = {}
        
        if startDateTime != None and endDateTime != None:
            filter['chippingDateTime__range'] = (startDateTime, endDateTime)

        elif startDateTime != None:
            filter['chippingDateTime__gte'] = startDateTime
        
        elif endDateTime != None:
            filter['chippingDateTime__lte'] = endDateTime


        if(chipperId != None):
            filter['chipperId'] = chipperId
            
        if(chippingLocationId != None):
            filter['chippingLocationId'] = chippingLocationId
            
        if(lifeStatus != None):
            filter['lifeStatus'] = lifeStatus
            
        if(gender != None):
            filter['gender'] = gender

        '''
            TODO: Optimize if statments
            END
        '''

        # Filter by query_params
        queryset = Animal.objects.filter(**filter).order_by('-id').reverse()

        return queryset[from_:from_+size]