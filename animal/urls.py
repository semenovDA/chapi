from django.urls import path, include, re_path
from .views import *

app_name = "animals"

urlpatterns = [
    path('', include('animal_type.urls')),
    path('', include('animal_location.urls')),
    re_path(r'^animals/(?P<pk>-?\d+)$', AnimalDetail.as_view()),
    path('animals/search', AnimalList.as_view()),
    path('animals', CreateAnimal.as_view()),
]