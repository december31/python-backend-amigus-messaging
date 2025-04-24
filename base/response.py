from django.http import JsonResponse
from rest_framework.response import Response
from base.status import HttpStatus


class BaseResponse:
    @staticmethod
    def create(http_status: HttpStatus, data: object = None):
        return JsonResponse(
            status=http_status.status,
            data={
                'code': http_status.code,
                'message': http_status.message,
                'data': data,
            }
        )


class BaseListResponse:
    @staticmethod
    def create(http_status: HttpStatus, page: int, page_size: int, data: object = None):
        return JsonResponse(
            status=http_status.status,
            data={
                'code': http_status.code,
                'message': http_status.message,
                'page': page,
                'page_size': page_size,
                'data': data,
            }
        )
