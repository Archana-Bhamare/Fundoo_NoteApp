from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Registration(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=65)
