from utils.exception_handler import BaseApiException
from utils.status import user_not_found


class UserNotFoundException(BaseApiException):
    status = user_not_found
