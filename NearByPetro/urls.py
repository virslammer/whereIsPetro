from django.urls import path
from .views import Index,ShowNearByPetro
urlpatterns = [
    path('',Index,name='index'),
    path('shownearbypetro/',ShowNearByPetro,name='show-nearby')
]