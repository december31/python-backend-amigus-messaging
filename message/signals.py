
from django.dispatch import receiver
from django.db.models.signals import post_save

from message.models import Conversation, Message

@receiver(post_save, sender=Message)
def on_message_saved(sender, instance, created, **kwargs):
    if created:
        instance.conversation.newest_message_time = instance.created_at
        instance.conversation.save()