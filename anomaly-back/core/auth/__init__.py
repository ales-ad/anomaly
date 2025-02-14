from contextvars import ContextVar
from functools import wraps
from typing import Optional

from config import config


from apps.users.models import AuthUser
from apps.users.services import  TokensService
from apps.users.exceptions import InvalidTokenErr

from .exceptions import PermissionDeniedErr


class AuthHeaderStore:
    def __init__(self):
        self._authorization_header: ContextVar[str] = ContextVar("authorization_header", default="")

    def set_authorization_header(self, val):
        self._authorization_header.set(val)

    def get_authorization_headers(self):
        return self._authorization_header.get()




auth_header_store = AuthHeaderStore()


class Auth:
    def __init__(self):
        self._user: ContextVar[AuthUser | None] = ContextVar("current_user", default=None)

    def set_user(self, val):
        self._user.set(val)

    @property
    def user(self) -> AuthUser:
        return self._user.get()

    def __call__(
            self,
            tgapp: bool = False,
            system: bool = False,
            roles: Optional[list[str]] = None,
            strict: bool = True,
            jwt_auth_allowed: bool = True
    ):
        def wrapper1(func):
            @wraps(func)
            async def wrapper2(*args, **kwargs):
                auth_header: str = auth_header_store.get_authorization_headers() or ""
               

                if not (
                        (jwt_auth_allowed and auth_header[:7] == 'Bearer ')
                ):
                    if strict:
                        raise InvalidTokenErr
                    else:
                        return await func(*args, **kwargs)

                token = auth_header[7:]

                if system:
                    if token != config.Auth.system_api_secret:
                        raise PermissionDeniedErr
                    return await func(*args, **kwargs)
                if tgapp:
                    if token != config.Auth.tgapp_api_secret:
                        raise PermissionDeniedErr
                    return await func(*args, **kwargs)

                if  token and jwt_auth_allowed:
                    auth_user = TokensService.decode_access_token(token)
                    self.set_user(auth_user)
                else:
                    raise RuntimeError

                if roles: 
                    if self.user.role in roles:
                            return await func(*args, **kwargs)

                    raise PermissionDeniedErr
                else:
                    # Если не установлен ни один параметр, значит запрос без проверки роли
                    return await func(*args, **kwargs)
            return wrapper2
        return wrapper1

    def get_user(
            self,
            tgapp: bool = False,
            system: bool = False,
            roles: Optional[list[str]] = None,
            strict: bool = True,
            jwt_auth_allowed: bool = True
    ):
        @self(
            tgapp=tgapp,
            system=system,
            roles=roles,
            strict=strict,
            jwt_auth_allowed=jwt_auth_allowed
        )
        async def fake_request() -> AuthUser:
            return self.user

        return fake_request

auth = Auth()

# Shortcuts
user_access = auth.get_user()
non_strict_access = auth.get_user(strict=False)
system_access = auth.get_user(system=True)
admin_access = auth.get_user(roles=["admin","moderator"])
