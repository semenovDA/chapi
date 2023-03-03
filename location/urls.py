from django.urls import path, re_path
from .views import *

app_name = "locations"

urlpatterns = [
    path('locations', CreateLocation.as_view()),
    re_path(r'^locations/(?P<pk>-?\d+)', LocationDetail.as_view())
]