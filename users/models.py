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

class AuthorApplication(models.Model):
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='author_application',
        verbose_name='Applicant'
    )

    reason = models.TextField(
        help_text='why do you want to become an author'

    )
    sample_of_work = models.FileField(upload_to='author_samples/', blank=True, null=True)

    STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    }
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default= 'pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Author Application'
        verbose_name_plural = 'Author Applications'
        permissions = [
            ("can_approve_author_applications", "can approve author applications"),
        ]
    def __str__(self):
        return f"Application from {self.user.username} - {self.get_status_display()}"    

        