from django.urls import path
from .views import rentalsPage, rentalDetailsPage

urlpatterns = [
    path("", rentalsPage, name='rentals'),
    path('<str:pk>/', rentalDetailsPage, name='rental_detail'),
]
