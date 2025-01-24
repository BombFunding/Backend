
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification

@receiver(post_save, sender=Notification)
def push_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(instance.user.id),
            {
                "type": "notification_message",
                "content": {
                    "message": instance.message,
                    "created_at": instance.created_at.isoformat(),
                    "type": instance.type,
                },
            },
        )