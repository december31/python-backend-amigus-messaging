import re
import string

from rest_framework import serializers


def password_validator(value: string):
    if len(value) < 8:
        raise serializers.ValidationError("Password must contain at least 8 characters")
    return value


def identifier_validator(value):
    """
    Custom validation for the identifier.
    Checks if it's a valid email or a basic phone number format.
    For production, use a more robust phone number validation library
    like `phonenumbers` if dealing with international numbers.
    """
    # Basic email regex validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Basic phone number regex (starts with + or is digits, 9-15 characters)
    # This is a very permissive regex. For production, consider country-specific validation.
    phone_regex = r'^\+?[0-9]{9,15}$'

    if re.fullmatch(email_regex, value):
        return value
    elif re.fullmatch(phone_regex, value):
        return value
    else:
        raise serializers.ValidationError('Invalid email or phone number')


def otp_validator(value):
    if value and value.isdigit():
        return value
    else:
        raise serializers.ValidationError("Otp is invalid")
