from typing import Optional

from django.contrib.auth.base_user import BaseUserManager
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token

from base.response import token_is_not_valid
from user import models
from utils.base_exception import BaseApiException


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)


class Authentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]:
        return super().authenticate(request)

    def get_validated_token(self, raw_token: bytes) -> Token:
        token = super().get_validated_token(raw_token)

        saved_token = models.Token.objects.get(access_token=raw_token.decode("utf-8"))

        if saved_token is None or saved_token.revoked:
            raise BaseApiException.create(token_is_not_valid)

        if saved_token.is_one_time_token:
            saved_token.revoked = True

        return token


class AuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = Authentication  # Link to the JWTAuthentication class
    name = 'jwtAuth'  # A unique name for this authentication scheme in the schema
    priority = -1  # Adjust priority if needed for multiple auth schemes

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
