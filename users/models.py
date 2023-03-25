from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True, max_length=500)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
