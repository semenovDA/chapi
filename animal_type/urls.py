from django.urls import path, re_path
from .views import *

app_name = "animal_types"

urlpatterns = [
    # AnimalType requests only
    re_path(r'^animals/types$', CreateAnimalType.as_view()),
    re_path(r'^animals/types/(?P<pk>-?\d+)$', AnimalTypeDetail.as_view()),

    # AnimalType & Animal requests combination only
    re_path(r'^animals/(?P<animalId>-?\d+)/types$', AnimalTypeEdition.as_view()), # /$ remove from end
    re_path(r'^animals/(?P<animalId>-?\d+)/types/(?P<typeId>-?\d+)$', AnimalTypeAddition.as_view())
]