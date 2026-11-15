from django.urls import path
from . import views


app_name = 'services'

urlpatterns = [
    path('', views.pokemon_view, name='pokemon'),
    path('remove/<str:pokemon_name>/', views.remove_pokemon,
         name='remove_pokemon'),
    path('dogs/', views.dogs_view, name='dogs'),
]
