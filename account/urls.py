from .views import *
from django.urls import path, re_path

urlpatterns = [
    path('registration', RegisterAPI.as_view()),
    re_path(r'^accounts/(?P<pk>-?\d+)', AccountDetail.as_view()),
    path('accounts/search', AccountList.as_view()),
]