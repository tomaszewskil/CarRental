from django.shortcuts import render
from rentals.models import Rental
from cars.models import CarTypes


# Create your views here.
def homePage(request):
    rentals = Rental.objects.all().order_by('name')
    cars = CarTypes.objects.all()
    context = {'rentals': rentals,
               'cars': cars}
    return render(request, 'home.html', context)


def aboutUsPage(request):
    return render(request, 'about_us.html')
