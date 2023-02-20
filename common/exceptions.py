from rest_framework.exceptions import APIException


class ObjectNotFoundException(APIException):
    status_code = 404


class UniqueObjectException(APIException):
    status_code = 400


class ObjectDeletedException(APIException):
    status_code = 400


class TypeErrorException(APIException):
    status_code = 400

class IncorrectCodeException(APIException):
    status_code = 400


class IncorrectPasswordException(APIException):
    status_code = 400


class IncorrectIDTokenException(APIException):
    status_code = 400


class UserAlreadyExist(APIException):
    status_code = 400

class SomethingGetWrongException(APIException):
    status_code = 400
