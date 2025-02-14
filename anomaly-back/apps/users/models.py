from enum import Enum

from pydantic import BaseModel, Field
from tortoise import Model, fields

class RoleEnum(str, Enum):
    client = "client"
    admin = "admin"
    moderator = "moderator"

class User(Model):
    class Meta:
        table = "users"

    id = fields.BigIntField(pk=True)
    phone = fields.CharField(max_length=31, null=True)
    role = fields.CharField(max_length=31, null=True)
    login = fields.CharField(max_length=127, null=True, unique=True)
    password = fields.CharField(max_length=127, null=True, unique=False)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class UserSession(Model):
    class Meta:
        table = "user_sessions"

    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User")
    user_id: int  
    refresh_token = fields.CharField(max_length=255, null=True)
    last_refresh = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class AuthUser(BaseModel):
    id: int
    role: RoleEnum | None = Field(
        None,
        description="Роль"
    )