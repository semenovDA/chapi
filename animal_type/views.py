from rest_framework.response import Response
from rest_framework import generics, status

from .models import AnimalType
from .serializers import AnimalTypeSerializer

from animal.models import Animal
from animal.serializers import AnimalSerializer

from core.exceptions import *
from core.utils import validate_dict_number
from core.permissions import CustomPermission


# POST on http://localhost:8000/animals/types
class CreateAnimalType(generics.CreateAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    permission_classes = (CustomPermission,)

# GET, PUT, DELETE on http://localhost:8000/animals/types/{typeId}
class AnimalTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (CustomPermission,)

    def delete(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk"))
        if(Animal.objects.filter(animalTypes__in=[pk]).exists()):
            raise BadRequestException('AnimalType is used by animal')

        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)    

# POST, DELETE on http://localhost:8000/animals/{animalId}/types/{typeId}
class AnimalTypeAddition(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    http_method_names = ['delete', 'post']
    permission_classes = (CustomPermission,)

    def post(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId"))
        typeId = int(kwargs.get("typeId"))

        try:
            animal = Animal.objects.get(pk=animalId)
            AnimalType.objects.get(pk=typeId)

        except Exception as e:
            raise NotFoundException(e.args)

        # Handle duplicates
        if(animal.animalTypes.filter(id=typeId).exists()):
            raise BadRequestException('typeId already in animal animalTypes')
        
        animal.animalTypes.add(typeId)
        animal.save()

        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

        
    def delete(self, request, *args, **kwargs):
        
        animalId = int(kwargs.get("animalId"))
        typeId = int(kwargs.get("typeId"))

        try:
            animal = Animal.objects.get(pk=animalId)
            AnimalType.objects.get(pk=typeId)

            if(not animal.animalTypes.filter(id=typeId).exists()):
                raise NotFoundException('typeId is not in animalTypes')

        except Exception as e:
            raise NotFoundException(e.args)
        
        if(animal.animalTypes.count() == 1):
            raise BadRequestException('Cannot delete the last type in animal')

        animal.animalTypes.remove(typeId)
        animal.save()

        serializer = AnimalSerializer(animal)

        return Response(serializer.data, status=status.HTTP_200_OK)


# PUT on http://localhost:8000/animals/{animalId}/types
class AnimalTypeEdition(generics.UpdateAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    http_method_names = ['put']
    permission_classes = (CustomPermission,)

    def put(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId"))

        if not validate_dict_number(request.data):
            raise BadRequestException('Invalid request body')

        try:
            animal = Animal.objects.get(pk=animalId)
            animal_type = AnimalType.objects.get(pk = request.data['newTypeId'])

        except Exception as e:
            raise NotFoundException(e.args)
    
        if not animal.animalTypes.filter(pk=request.data['oldTypeId']).exists():
            raise NotFoundException('[PUT AnimalTypeEdition] oldTypeId not found in animal.animalTypes')

        if animal.animalTypes.filter(pk=request.data['newTypeId']).exists():
            raise ConflictExistsException('[PUT AnimalTypeEdition] newTypeId is already in animal.animalTypes')

        animal.animalTypes.remove(request.data['oldTypeId'])
        animal.animalTypes.add(animal_type)
        animal.save() # TODO: should i use save after changing object 
        
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)