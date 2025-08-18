import string
from typing import Union

from django.core.cache import cache


def set_otp(identifier: str, otp_code: Union[str, None]):
    cache.set(f"otp_{identifier}", otp_code)


def get_otp(identifier: string):
    return cache.get(f"otp_{identifier}")


def set_otp_requested_timestamp(identifier: str, timestamp: Union[float, None]):
    cache.set(f"otp_requested_time_{identifier}", timestamp)


def get_otp_requested_timestamp(identifier: str):
    return cache.get(f"otp_requested_time_{identifier}")
