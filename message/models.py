from django.db import models

from base.models import BaseModel
from user.models import User


class Conversation(BaseModel):
    class TypeChoice(models.TextChoices):
        PRIVATE = "private", "Private"
        GROUP = "group", "Group"

    type = models.CharField(choices=TypeChoice.choices)
    name = models.CharField(null=True)


class ConversationRole(BaseModel):
    class NameChoice(models.TextChoices):
        ADMIN = "admin", "Admin"
        MODERATOR = "moderator", "Moderator"
        MEMBER = "member", "Member"

    name = models.CharField(choices=NameChoice.choices, unique=True)
    permissions = models.JSONField(default=list)


class ConversationParticipant(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="participants",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="conversation_member",
    )

    role = models.ForeignKey(ConversationRole, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)


class Message(BaseModel):
    class StatusChoice(models.TextChoices):
        SENT = "sent", "Sent"
        RECEIVED = "received", "Received"
        SEEN = "seen", "Seen"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="messages",
    )
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoice.choices, default=StatusChoice.SENT.value)

    @property
    def attachments(self):
        return Attachment.objects.filter(message=self)


class Attachment(BaseModel):
    class MimeTypeChoice(models.TextChoices):
        IMAGE = "image/*", "Image",
        AUDIO = "audio/*", "Audio"
        FILE = "application/*", "File"

    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=255)
    mime_type = models.CharField(choices=MimeTypeChoice.choices)
