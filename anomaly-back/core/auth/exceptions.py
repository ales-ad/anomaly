from core.exceptions import BaseAppException


class PermissionDeniedErr(BaseAppException):
    status_code = 403
