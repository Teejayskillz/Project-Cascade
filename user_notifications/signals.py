from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify
from users.models import Subscribe  # Make sure to import the new model name

@receiver(post_save, sender=Subscribe)
def send_subscription_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(
            instance.subscriber,  # actor: the user who subscribed
            recipient=instance.subscribed_to,  # who gets the notification: the user being subscribed to
            verb=f"started subscribing to you."
        )