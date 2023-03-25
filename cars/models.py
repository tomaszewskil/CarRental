from django.db import models
from rentals.models import Rental
from users.models import CustomUser


# Create your models here.
class CarTypes(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Gas', 'Gas'),
        ('Diesel', 'Diesel')
    ]

    GEARBOX_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual')
    ]

    DRIVE_CHOICES = [
        ('FWD', 'Front Wheel Drive'),
        ('AWD', 'All Wheel Drive'),
        ('RWD', 'Rear Wheel Drive')
    ]

    producer = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    fuel = models.CharField(max_length=10, choices=FUEL_CHOICES)
    seats = models.PositiveIntegerField()
    gearbox = models.CharField(max_length=10, choices=GEARBOX_CHOICES)
    drive = models.CharField(max_length=3, choices=DRIVE_CHOICES)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.producer + " " + self.type


class Car(models.Model):
    carType = models.ForeignKey(CarTypes, on_delete=models.CASCADE)
    rentals = models.ForeignKey(Rental, on_delete=models.CASCADE)

    def __str__(self):
        return self.carType.__str__() + " (SN: " + self.id.__str__() + ") - " + self.rentals.__str__()


class RentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    add_fuel = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " " + self.car.carType.producer + " " + self.car.carType.type
