from django.db import models


# Create your models here.

class Rental(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    street_number = models.PositiveIntegerField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    open_hours = models.TextField(default="Open hours coming soon... ")
    description = models.TextField(max_length=500, default="Description coming soon... ")
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
