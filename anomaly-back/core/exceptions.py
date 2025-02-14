class BaseAppException(Exception):
    status_code = 422
    error_desc = None

    def __str__(self):
        return self.__class__.__name__

    def err_info(self):
        return None


class IncorrectlyParameters(BaseAppException):
    status_code = 400
