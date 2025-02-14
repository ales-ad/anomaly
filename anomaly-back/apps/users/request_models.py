from typing import Optional
from pydantic import BaseModel

from .models import RoleEnum

class UserAuthRequest(BaseModel):
    login: str
    password: str


class UserCreateRequest(BaseModel):
    login: str
    password: str
    role: RoleEnum

class UserUpdateRequest(BaseModel):
    login: str
    password: Optional[str] = None
    role: RoleEnum

class UserUpdatePatchRequest(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserDataRequest(BaseModel):
    id: int
    login: str
    role: str


class LoginSessionCompleteResponse(BaseModel):
    access_token: str
    refresh_token: str

class UserDataListView(BaseModel):
    items: list[UserDataRequest]
    total: int