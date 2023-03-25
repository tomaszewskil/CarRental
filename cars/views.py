from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import RentHistoryForm
from django.contrib.auth import get_user_model
from .filters import CarsTypesFilter


# Create your views here.
def carsPage(request):
    carTypes = CarTypes.objects.all()
    carTypesFilter = CarsTypesFilter(request.GET, queryset=carTypes)
    context = {'carTypesFilter': carTypesFilter}
    return render(request, 'cars.html', context)


def carDetailsPage(request, pk):
    car = CarTypes.objects.get(id=pk)
    rentals = Rental.objects.filter(car__carType=pk).distinct().order_by('name')
    context = {'car': car,
               'rentals': rentals}
    return render(request, 'car_details.html', context)


@login_required(login_url='login')
def carRentPage(request, pk):
    car = CarTypes.objects.get(id=pk)
    form = RentHistoryForm(car_type=pk)
    if request.method == 'POST':
        form = RentHistoryForm(pk, request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User.objects.filter(username=request.user.get_username()).first()
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            rental = request.POST.get('rental')
            rented_cars = Car.objects.filter(renthistory__start_date__lte=end_date,
                                             renthistory__end_date__gte=start_date)

            available_cars = Car.objects.filter(rentals=rental, carType=pk).difference(rented_cars)
            car = available_cars.first()

            if request.POST.get('add_fuel') == 'on':
                add_fuel = True
            else:
                add_fuel = False
            transaction = RentHistory(user=user, car=car, start_date=start_date, end_date=end_date, add_fuel=add_fuel)
            transaction.save()
            return redirect('rent_history', request.user.get_username())

    context = {'form': form,
               'car': car}
    return render(request, 'car_rent.html', context)
