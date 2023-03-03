from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from .models import AnimalType
from animal.models import Animal
from animal.serializers import AnimalSerializer

from .serializers import AnimalTypeSerializer
from core.exceptions import *
from core.utils import ValidateDict

# POST on http://localhost:8000/animals/types
class CreateAnimalType(generics.CreateAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    
    def post(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')
        return self.create(request, *args, **kwargs)

# GET, PUT, DELETE on http://localhost:8000/animals/types/{typeId}
class AnimalTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    http_method_names = ['get', 'put', 'delete']

    def post(self, request, *args, **kwargs):
        raise ValueError('POST')

    def get(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0))

        if(pk <= 0):
            raise BadRequestException('AnimalType should not be negitive or null')

        try:
            animal_type = AnimalType.objects.get(pk=pk)
            serializer = AnimalTypeSerializer(animal_type)
            return Response(serializer.data) 

        except AnimalType.DoesNotExist:
            raise NotFoundException('Animal type not found')
    
    def put(self, request, *args, **kwargs):

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk", 0))
        if(pk <= 0):
            raise BadRequestException('AnimalType should not be negitive or null')
        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

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

    def post(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))
        typeId = int(kwargs.get("typeId", 0))

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if(animalId <= 0):
            raise BadRequestException('animalId should not be null or negitive')
 
        if(typeId <= 0):
            raise BadRequestException('typeId should not be null or negitive')

        try:
            animal = Animal.objects.get(pk=animalId)
            AnimalType.objects.get(pk=typeId)

        except Exception as e:
            raise NotFoundException('AnimalId or AnimalType not found')

        # Handle duplicates
        if(animal.animalTypes.filter(id=typeId).count() != 0):
            raise BadRequestException('typeId already in animal animalTypes')
        
        animal.animalTypes.add(typeId)
        animal.save()

        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

        
    def delete(self, request, *args, **kwargs):
        
        animalId = int(kwargs.get("animalId", 0))
        typeId = int(kwargs.get("typeId", 0))

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if(animalId <= 0):
            raise BadRequestException('animalId should not be null or negitive')
 
        if(typeId <= 0):
            raise BadRequestException('typeId should not be null or negitive')

        try:
            animal = Animal.objects.get(pk=animalId)
            AnimalType.objects.get(pk=typeId)
            if(not animal.animalTypes.filter(id=typeId).exists()):
                raise NotFoundException('typeId is not in animalTypes')

        except Exception as e:
            raise NotFoundException(e.args)
        
        if(animal.animalTypes.count() == 1 and animal.animalTypes.first().id == typeId):
            raise BadRequestException('Cannot delete the last type in animal')

        animal.animalTypes.remove(typeId)
        animal.save()

        serializer = AnimalSerializer(animal)

        return Response(serializer.data, status=status.HTTP_200_OK)


# PUT on http://localhost:8000/animals/{animalId}/types
class AnimalTypeEdition(generics.RetrieveAPIView):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    http_method_names = ['put', 'post']

    def put(self, request, *args, **kwargs):
        animalId = int(kwargs.get("animalId", 0))

        if(request.user.is_authenticated != True): # Проверка на авторизованность
            raise AuthenticationException('Неверные авторизационные данные')

        if(animalId <= 0):
            raise BadRequestException('animalId cannot be null or negitive')

        if not ValidateDict(request.data):
            raise BadRequestException('[PUT AnimalTypeEdition] Should not be null or negitive')

        try:
            animal = Animal.objects.get(pk=animalId)
            AnimalType.objects.get(pk = request.data['newTypeId'])

            if not animal.animalTypes.filter(pk=request.data['oldTypeId']).exists():
                raise NotFoundException('[PUT AnimalTypeEdition] oldTypeId not found in animal.animalTypes')

            if animal.animalTypes.filter(pk=request.data['newTypeId']).exists():
                raise ConflictExistsException('[PUT AnimalTypeEdition] newTypeId is already in animal.animalTypes')

            # TODO: Can be removed ?
            types = list(request.data.values())
            if animal.animalTypes.filter(id__in=types).count() == len(types):
                raise ConflictExistsException('[PUT AnimalTypeEdition] newTypeId and oldTypeId is already in animal.animalTypes')

        except Exception as e: # TODO: Handle exceptions here
            if type(e) == ConflictExistsException or type(e) == NotFoundException:
                raise e
            else:
                raise NotFoundException(e.args)
    
        # TODO: Should be replaced not removed
        arr = list(t.id for t in animal.animalTypes.all())
        arr[arr.index(request.data['oldTypeId'])] = request.data['newTypeId']
        animal.animalTypes.set(arr)
        animal.save()
        
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)