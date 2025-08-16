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

class Profile(models.Model):
    user = models.OneToOneField(userRegistration, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg',blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user__username']