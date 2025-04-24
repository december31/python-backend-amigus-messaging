from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.conf.urls import handler404
import logging
from base import status

from base.response import BaseResponse
from base.status import HttpStatus, internal_server_error, not_found

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
   Custom handler for DRF exceptions. Wraps all errors in a consistent response structure.
   Handles both standard DRF errors and unexpected internal server errors (500).
   """

    # Call DRF's built-in exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        return BaseResponse.create(
            http_status=HttpStatus(
                response.status_code,
                response.status_code,
                response.message
            ),
            data=None
        )
    else:
        # Internal server error (uncaught by DRF)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        return BaseResponse.create(
            internal_server_error,
            data=None
        )


def custom_404_view(request, exception=None):
    return BaseResponse.create(not_found)


def custom_500_view(request, exception=None):
    return BaseResponse.create(internal_server_error)
