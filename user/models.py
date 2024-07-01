import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):

    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    is_librarian = models.BooleanField(default=False)
  