from rest_framework.exceptions import APIException

from base.response import internal_server_error


class BaseApiException(APIException):
    status = internal_server_error

    @staticmethod
    def create(status):
        exception = BaseApiException()
        exception.status = status
        return exception
