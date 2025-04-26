from django.utils import timezone
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields for tracking creation and updates.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the record was created."
    )

    updated_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the record was updated."
    )

    class Meta:
        abstract = True
