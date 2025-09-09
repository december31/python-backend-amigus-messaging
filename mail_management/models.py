from django.contrib.auth import get_user_model
from django.db import models

from base.models import BaseModel

User = get_user_model()

# Create your models here.
class MailLog(BaseModel):
    class StatusChoice(models.TextChoices):
        PENDING = "PENDING", "pending"
        SUCCESS = "SUCCESS", "success"
        FAILURE = "FAILURE", "failure"
        SENDING = "SENDING", "sending"

    subject = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(choices=StatusChoice.choices, max_length=10)
    error_message = models.TextField(null=True)
    sent_at = models.DateTimeField(null=True)
    receiver = models.EmailField()
