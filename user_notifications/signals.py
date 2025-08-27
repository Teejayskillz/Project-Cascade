from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify
from users.models import Follow

@receiver(post_save, sender=Follow)
def send_follow_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(
            instance.follower,  # actor
            recipient=instance.following,  # who gets the notification
            verb=f"started following you."
        )
