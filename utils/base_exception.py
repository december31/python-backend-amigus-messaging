from rest_framework.exceptions import APIException

from base.response import internal_server_error


class BaseApiException(APIException):
    status = internal_server_error
    message = status.message

    @staticmethod
    def create(status, message: str | None = None):
        exception = BaseApiException()
        exception.status = status
        exception.message = message or status.message
        return exception
