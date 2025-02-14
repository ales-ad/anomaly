import random

import traceback
from passlib.context import CryptContext

from typing import Any

from tortoise.backends.base_postgres.client import BasePostgresClient
from datetime import datetime, timedelta, timezone, UTC
from urllib.parse import parse_qsl, unquote

from tortoise.transactions import in_transaction
from tortoise.expressions import F
import jwt

from core import db
from config import config
from core.db import sql, get_connection
from core.logger import log

from ..request_models import (
    UserAuthRequest,
    LoginSessionCompleteResponse
)
from ..exceptions import (
    UserNotFoundErr,
    TokenExpiredErr,
    InvalidTokenErr,
    SessionExpiredErr,
    SessionNotFoundErr,
    InvalidUserPasswordErr
)
from ..models import User, AuthUser, UserSession


class UserService:
    @staticmethod
    def verify_user_password(user, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, user.password)

    @classmethod
    async def check_password(cls, login: str, password: str) -> User:
        async with db.Transaction() as con:
            _params = {
                    'login': login
                }
            user = await User.filter(**_params).using_db(con).first()
            if user:
                if cls.verify_user_password(user,password):
                    return user 
                else:
                    raise InvalidUserPasswordErr
            else:
                raise UserNotFoundErr
        
class AuthService:
    @classmethod
    async def complete_login_session(
            cls,
            request: UserAuthRequest
    ) -> LoginSessionCompleteResponse:
        async with in_transaction() as con:
            
            r = await cls._complete_login_session(
                transaction_con=con,
                login=request.login,
                password=request.password
            )
  
            if isinstance(r, Exception):
                raise r
            else:
                access, refresh = r
                return LoginSessionCompleteResponse(
                    access_token=access,
                    refresh_token=refresh
                )
        

    @classmethod
    async def _complete_login_session(
            cls,
            transaction_con: BasePostgresClient,
            login: str,
            password: str,
            create_auth_session: bool = True
    ) -> tuple[str, str] | AuthUser:
        con = transaction_con

        user = await UserService.check_password(login, password)
        
        if user.deleted_at:
                raise UserNotFoundErr
        
        auth_user = AuthUser(
                id=user.id,
                role=user.role,
        )
   
        if create_auth_session:
                session = UserSession(
                    user_id=user.id
                )
                await session.save(using_db=con)
           
                refresh_token = TokensService.generate_refresh_token(session.id)
                session.refresh_token = refresh_token
                await session.save(using_db=con)
             
                # delete old sessions
                await con.execute_query(
                    f"""
                    DELETE FROM {UserSession.Meta.table} us
                    WHERE us.id IN (
                        SELECT us2.id FROM {UserSession.Meta.table} us2 WHERE us2.user_id=$1
                        ORDER BY id DESC OFFSET 5
                    )
                    """,
                    [user.id]
                )

                return TokensService.generate_access_token(auth_user), refresh_token
        else:
                return auth_user

    @staticmethod
    async def create_session(user_id: int) -> int:
        code = random.randint(100000, 999999)
        async with db.Transaction() as con:
            _params = {
                    'id': user_id
                }
            user = await User.filter(**_params).using_db(con).first()
            if user is None:
                    raise UserNotFoundErr

            uls = UserSession(
                code=code,
                user=user,
     
            )
            await uls.save(using_db=con)
            return uls.id
        

class TokensService:
    @classmethod
    async def refresh_token(cls, refresh_token: str) -> tuple[str, str]:
        session_id = cls._decode_refresh_token(refresh_token)
        new_refresh_token = cls.generate_refresh_token(session_id)
        async with in_transaction() as con:
            us = await UserSession.filter(id=session_id, refresh_token=refresh_token)\
                .using_db(con).select_for_update().first()
            if us is None:
                raise SessionExpiredErr

            us.refresh_token = new_refresh_token
            us.last_refresh = datetime.now(timezone.utc)
            await us.save(using_db=con)

            rows = await con.execute_query_dict(
                f"""
                SELECT
                    u.id FROM users u
                WHERE u.id=$1
                """,
                [us.user_id, ]
            )

        user = rows[0] if len(rows) > 0 else None
        if not user:
            raise SessionNotFoundErr

        au = AuthUser(
            id=user["user_id"],
            role=user["user_role"],
        )
        return cls.generate_access_token(au), new_refresh_token

    @staticmethod
    def decode_access_token(token: str) -> AuthUser:
        try:
            payload = jwt.decode(token, algorithms=["HS256"], key=config.Auth.jwt_secret)
            return AuthUser(
                id=payload["user_id"],
                role=payload["user_role"],
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredErr
        except (
                ValueError,
                KeyError,
                jwt.InvalidTokenError,
                jwt.DecodeError,
                jwt.InvalidSignatureError,
                jwt.MissingRequiredClaimError,
        ):
            print(traceback.format_exc())
            raise InvalidTokenErr

    @staticmethod
    def generate_access_token(u: AuthUser) -> str:
        token_data = {
            "user_id": u.id,
            "user_role": u.role,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=config.Auth.access_token_life_time_seconds)
        }
        return jwt.encode(token_data, config.Auth.jwt_secret, algorithm="HS256")

    @staticmethod
    def generate_refresh_token(session_id: int) -> str:
        token_data = {
            "session_id": session_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=config.Auth.refresh_token_life_time_days)
        }
        return jwt.encode(token_data, config.Auth.jwt_secret, algorithm="HS256")


    @staticmethod
    def _decode_refresh_token(token: str) -> int:
        try:
            return jwt.decode(token, algorithms=["HS256"], key=config.Auth.jwt_secret)["session_id"]
        except jwt.ExpiredSignatureError:
            raise TokenExpiredErr
        except (
                ValueError,
                KeyError,
                jwt.InvalidTokenError,
                jwt.DecodeError,
                jwt.InvalidSignatureError,
                jwt.MissingRequiredClaimError,
        ):
            raise InvalidTokenErr
