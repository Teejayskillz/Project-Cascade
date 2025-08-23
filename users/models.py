# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# The single custom user model
class CustomUser(AbstractUser):
    # This field is for a fixed set of roles
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('staff', 'Staff'),
        ('regular', 'Regular User'),
    )        

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

# The separate profile model
class Profile(models.Model):
    # Link to the custom user model with a OneToOneField
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user__username']