from django.urls import path
from .views import carsPage, carDetailsPage, carRentPage

urlpatterns = [
    path("", carsPage, name='cars'),
    path("<str:pk>/", carDetailsPage, name='car_detail'),
    path('<str:pk>/rent/', carRentPage, name='car_rent'),
]
