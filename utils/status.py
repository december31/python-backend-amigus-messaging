from django.http import Http404
from rest_framework import status


class HttpStatus:
    def __init__(self, status_code: int, code: int, message: str):
        self.status = status_code
        self.code = code
        self.message = message


success = HttpStatus(status.HTTP_200_OK, code=200, message="success")
not_found = HttpStatus(status.HTTP_404_NOT_FOUND, code=404, message="not found")
internal_server_error = HttpStatus(status.HTTP_500_INTERNAL_SERVER_ERROR, code=500, message="internal server error")
user_not_found = HttpStatus(status.HTTP_404_NOT_FOUND, code=4041, message="user not found")
