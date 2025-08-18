import string

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.models import Token

User = get_user_model()
def generate_token(user: User):
    if not user.is_active:
        raise AuthenticationFailed("User is inactive")

    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)
