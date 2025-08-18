from django.http import Http404
from rest_framework.generics import get_object_or_404

from base.response import HttpStatus
from utils.exception_handler import BaseApiException


def get_object_or_exception(queryset, error_http_status: HttpStatus, *filter_args, **filter_kwargs):
    try:
        model = get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except Exception as e:
        if isinstance(e, Http404):
            raise BaseApiException.create(error_http_status)
        else:
            raise e

    return model
