from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here

class userRegistration(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User Registration'
        verbose_name_plural = 'User Registrations'
        ordering = ['username']
