from django.shortcuts import render
from .models import *


# Create your views here.
def rentalsPage(request):
    rentals = Rental.objects.all().order_by('city')
    context = {'rentals': rentals}
    return render(request, 'rentals.html', context)


def rentalDetailsPage(request, pk):
    rental = Rental.objects.get(id=pk)
    context = {'rental': rental}
    return render(request, 'rental_details.html', context)
