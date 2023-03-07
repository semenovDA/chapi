import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Animal
from .filters import AnimalFilter
from .serializers import AnimalSerializer

from core.exceptions import *
from core.utils import validate_dict_number
from core.permissions import CustomPermission

from animal_type.models import AnimalType
from location.models import Location
from account.models import Account

# POST on http://localhost:8000/animals
class CreateAnimal(generics.CreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (CustomPermission,)

    def post(self, request, *args, **kwargs):

        if not validate_dict_number(request.data):
            raise BadRequestException('Invalid values in request body')
        
        try:
            animalTypes = request.data['animalTypes']
            Account.objects.get(pk=request.data['chipperId'])
            Location.objects.get(pk=request.data['chippingLocationId'])
        
        except Exception as e:
            raise NotFoundException(e.args)

        if(len(list(set(animalTypes))) != len(animalTypes)):
            raise ConflictExistsException('animalTypes has duplicates')

        if AnimalType.objects.filter(id__in=animalTypes).count() != len(animalTypes):
            raise NotFoundException('animalTypes not found')

        return self.create(request, *args, **kwargs)

# GET, PUT, DELETE on http://localhost:8000/animals/{animalId}
class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (CustomPermission,)

    def put(self, request, *args, **kwargs):

        if not validate_dict_number(request.data):
            raise BadRequestException('Invalid request body')

        try:
            Account.objects.get(pk=request.data['chipperId'])
            Location.objects.get(pk=request.data['chippingLocationId'])

        except Exception as e:
            raise NotFoundException(e.args)

        instance = self.get_object()

        # LIFE STATUS HANDLING 
        if('lifeStatus' in request.data): # TODO: replace in db action

            if(request.data['lifeStatus'] == 'DEAD'):
                instance.deathDateTime = datetime.datetime.now().isoformat()
                instance.save()

            elif(instance.lifeStatus == 'DEAD' and request.data['lifeStatus'] == 'ALIVE'):
                raise BadRequestException('Cannot change DEAD status to ALIVE')

        # CHIPPING LOCATION HANDLING
        if(instance.visitedLocations.count() > 0):
            if(instance.visitedLocations.first().locationPointId.id == request.data['chippingLocationId']):
                raise BadRequestException('chippingLocationId should not be a first visitedLocation point')

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        instance = self.get_object()
        if(instance.visitedLocations.count() != 0):
            raise BadRequestException('Animal has visitLocations')

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
    queryset = Animal.objects.all().order_by('id')
    serializer_class = AnimalSerializer
    permission_classes = (CustomPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnimalFilter