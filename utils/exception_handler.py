import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, serializers
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

from base.response import BaseResponse, HttpStatus, internal_server_error, not_found, invalid_token, bad_request
from utils.base_exception import BaseApiException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
   Custom handler for DRF exceptions. Wraps all errors in a consistent response structure.
   Handles both standard DRF errors and unexpected internal server errors (500).
   """

    # Call DRF's built-in exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*exc.args)
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*exc.args)

    if isinstance(exc, BaseApiException):
        logger.error(f"Exception: {exc}", exc_info=True)
        return BaseResponse.create(
            http_status=exc.status,
            message=exc.message,
            data=None
        )

    if isinstance(exc, InvalidToken):
        logger.error(f"Exception: {exc}", exc_info=True)
        return BaseResponse.create(
            http_status=invalid_token,
            data=None
        )

    if isinstance(exc, serializers.ValidationError):
        errors = exc.detail
        error_messages = []

        if isinstance(errors, dict):
            for field, err_list in errors.items():
                if isinstance(err_list, list):
                    for err_msg in err_list:
                        error_messages.append(f"{field}: {err_msg}")
                else:
                    # For non-list errors
                    error_messages.append(f"{field}: {err_list}")
        else:
            # Handle non-dictionary errors (e.g., list of strings)
            error_messages = [str(err) for err in errors]

        if len(errors) == 0:
            error_messages.append("Bad request")

        return BaseResponse.create(
            http_status=bad_request,
            message=error_messages[0],
            data=None,
        )

    if response is not None:
        logger.error(f"Exception: {exc}", exc_info=True)
        return BaseResponse.create(
            http_status=HttpStatus(
                status_code=response.status_code,
                code=response.status_code,
                message=exc.detail,
            ),
            data=None
        )

    else:
        # Internal server error (uncaught by DRF)
        logger.error(f"Exception: {exc}", exc_info=True)

        return BaseResponse.create(
            internal_server_error,
            data=None
        )


def custom_404_view(request, exception=None):
    logger.error(f"Unhandled exception: {exception}", exc_info=True)
    return BaseResponse.create(not_found)


def custom_500_view(request, exception=None):
    logger.error(f"Unhandled exception: {exception}", exc_info=True)
    return BaseResponse.create(internal_server_error)
