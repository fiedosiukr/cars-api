from rest_framework import status
from rest_framework.exceptions import APIException


class CarNotFoundException(APIException):
    default_code = "error"
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The given car doesn't exist."


class CarAPIUnavailableException(APIException):
    default_code = "error"
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The given car doesn't exist."
