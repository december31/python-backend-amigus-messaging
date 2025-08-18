from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import Token

User = get_user_model()

from utils.validators import password_validator, identifier_validator, otp_validator


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("access_token", "refresh_token")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone", "avatar")

class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        max_length=255,
        help_text="User's phone number (e.g., +84912345678) or email address (e.g., user@example.com)",
        validators=[identifier_validator]
    )


class VerifyOtpSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        max_length=255,
        help_text="User's phone number (e.g., +84912345678) or email address (e.g., user@example.com)",
        validators=[identifier_validator]
    )

    otp = serializers.CharField(
        max_length=6,
        help_text="User's OTP code (e.g., 123456)",
        validators=[otp_validator]
    )


class SignUpSerializer(serializers.Serializer):
    identifier = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, validators=[password_validator])

class SignInSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, validators=[password_validator])

class UpdateUserInformationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(max_length=100)
