from django.urls import path, re_path
from .views import *


app_name = "animal_location"

urlpatterns = [
    re_path(r'^animals/(?P<animalId>-?\d+)/locations/(?P<pointId>-?\d+)$', AnimalLocationAddition.as_view()),
    re_path(r'^animals/(?P<animalId>-?\d+)/locations$', AnimalLocationList.as_view()),
]