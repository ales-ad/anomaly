from core.exceptions import BaseAppException



class UserNotFoundErr(BaseAppException):
    pass

class InvalidUserPasswordErr(BaseAppException):
    pass


class TokenExpiredErr(BaseAppException):
    pass


class InvalidTokenErr(BaseAppException):
    pass

class TgappAlreadySynced(BaseAppException):
    status_code = 400


class MainAccountSyncedWithAnotherTgapp(BaseAppException):
    status_code = 400


class TgappNotSynced(BaseAppException):
    status_code = 400

class SessionNotFoundErr(BaseAppException):
    pass


class SessionExpiredErr(BaseAppException):
    pass