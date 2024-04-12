from rest_framework import exceptions, status


class CustomValidationException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'
    default_detail = 'Ocorreu um erro'

    def __init__(self, detail=None, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.default_detail = detail
        self.status_code = status_code
        super().__init__(detail, code)