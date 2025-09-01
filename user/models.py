import logging
import string
import traceback
from importlib.metadata import requires
from logging import exception

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import ForeignKey

from base.models import BaseModel

logger = logging.getLogger(__name__)

class CustomUserManager(UserManager):
    def get_by_email_or_null(self, email):
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            logger.info(f"user with email: {email} does not existed, returning null . . .")
            return None

    def get_by_phone_or_null(self, phone):
        try:
            return self.get(phone=phone)
        except self.model.DoesNotExist:
            logger.info(f"user with phone: {phone} does not exist, returning null . . .")
            return None

    def create_superuser(
        self, email=..., password=..., **extra_fields
    ):
        super().create_superuser(username=email, email=email, password=password, **extra_fields)



class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(max_length=255, unique=True, null=True, blank=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=False)

    avatar = models.CharField(max_length=255, null=True, blank=True)

    is_initialized = models.BooleanField(default=False)

    objects = CustomUserManager()


class Token(BaseModel):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    is_one_time_token = models.BooleanField(default=False)
    revoked = models.BooleanField(default=False)
    owner = ForeignKey(User, on_delete=models.CASCADE)
