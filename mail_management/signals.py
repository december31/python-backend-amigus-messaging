import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from mail_management.models import MailLog
from mail_management.tasks import send_mail_async

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MailLog)
def on_mail_log_saved(sender, instance, created, **kwargs):
    logger.info(f"MailLog saved: {instance}")
    if created and instance.status == MailLog.StatusChoice.PENDING.value:
        send_mail_async.delay(instance.id)
