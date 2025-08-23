from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile whenever a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # This part ensures that the profile is saved when the user object is updated.
        instance.profile.save()