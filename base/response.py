import json
import string

from django.http import JsonResponse

from rest_framework import status


class HttpStatus:
    def __init__(self, status_code: int, code: int, message: str):
        self.status = status_code
        self.code = code
        self.message = message


success = HttpStatus(status.HTTP_200_OK, code=200, message="success")
created = HttpStatus(status.HTTP_201_CREATED, code=201, message="created")

not_found = HttpStatus(status.HTTP_404_NOT_FOUND, code=404, message="not found")
user_not_found = HttpStatus(status.HTTP_404_NOT_FOUND, code=4041, message="user not found")

internal_server_error = HttpStatus(status.HTTP_500_INTERNAL_SERVER_ERROR, code=500, message="internal server error")

too_many_request = HttpStatus(status.HTTP_429_TOO_MANY_REQUESTS, code=429, message="too many requests")
otp_request_is_cooling_down = HttpStatus(status.HTTP_429_TOO_MANY_REQUESTS, code=4291, message="otp request is cooling down")

otp_is_not_correct = HttpStatus(status.HTTP_401_UNAUTHORIZED, code=4011, message="otp is not correct")
otp_has_not_been_requested = HttpStatus(status.HTTP_401_UNAUTHORIZED, code=4012, message="otp has not been requested")
otp_has_expired = HttpStatus(status.HTTP_401_UNAUTHORIZED, code=4013, message="otp has expired")

class BaseResponse:

    def __init__(self, code: int, message: string, data: object):
        self.code = code
        self.message = message
        self.data = data

    @staticmethod
    def create(http_status: HttpStatus, message: string = None, data=None) -> JsonResponse:
        if data is None:
            data = {}
        return JsonResponse(
            status=http_status.status,
            data={
                "code": http_status.code,
                "message": message if message else http_status.message,
                "data": data
            }
        )


class BaseListResponse:
    @staticmethod
    def create(http_status: HttpStatus, data: object = None) -> JsonResponse:
        return JsonResponse(
            status=http_status.status,
            data={
                "code": http_status.code,
                "message": http_status.message,
                "data": data
            }
        )


class BasePagedListResponse:
    @staticmethod
    def create(http_status: HttpStatus, page: int, page_size: int, data: object = None) -> JsonResponse:
        return JsonResponse(
            status=http_status.status,
            data={
                "code": http_status.code,
                "message": http_status.message,
                "page": page,
                "page_size": page_size,
                "data": data
            }
        )
