from django.urls import path
from . import views

urlpatterns = [
    path('foods/', views.food_list_view, name='food_list'),
    path('foods/custom/add/', views.add_custom_food_view, name='add_custom_food'),
]