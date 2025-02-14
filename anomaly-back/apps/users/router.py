from fastapi import APIRouter, Query, Depends

from core.auth import admin_access, AuthUser

from core.response import AppResponse
from core.pagination import RequestQueryPaginate

from .request_models import (
    LoginSessionCompleteResponse,
    UserAuthRequest,
    UserCreateRequest,
    UserDataRequest,
    UserDataListView,
    UserUpdateRequest,
    UserUpdatePatchRequest
    )
from .services import AuthService, UserService




router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/auth",
    summary="Авторизация по логину и паролю",
    description="Авторизация уже зарегистрированного пользователя в системе по логину и паролю",
    response_model=AppResponse[LoginSessionCompleteResponse]
)
async def users_password_login(req: UserAuthRequest):
    return AppResponse[LoginSessionCompleteResponse](
        data=await AuthService.complete_login_session(request=req)
    )


@router.get(
    "/detail/{user_id}",
    summary="данные пользователя",
    response_model=AppResponse[UserDataRequest]
)
async def create_user(user_id: int):
    item =  await UserService.detail(user_id)
 
    return AppResponse[UserDataRequest](data=item)

@router.get(
    "/my",
    summary="Создание пользователя",
    response_model=AppResponse[UserDataRequest],
    dependencies=[Depends(admin_access)],

)
async def create_user(user: AuthUser = Depends(admin_access)):
    item =  await UserService.detail(user.id)
 
    return AppResponse[UserDataRequest](data=item)


@router.post(
    "/create",
    summary="Создание пользователя",
    response_model=AppResponse
)
async def create_user(req: UserCreateRequest):
    await UserService.create(req.login, req.password, req.role)
    return AppResponse()

@router.put(
    "/{user_id}",
    summary="Изменение",
    response_model=AppResponse
)
async def update_user(user_id: int, req: UserUpdateRequest):
    await UserService.update(id=user_id,login=req.login, role=req.role)
    return AppResponse()

@router.patch(
    "/{user_id}",
    summary="Изменение",
    response_model=AppResponse
)
async def update_user(user_id: int, req: UserUpdatePatchRequest):
    await UserService.patch(id=user_id,data=req)
    return AppResponse()

@router.delete(
    "/delete/{user_id}",
    summary="Удаление пользователя",
    response_model=AppResponse
)
async def delete(user_id: int):
    await UserService.delete(user_id)
 
    return AppResponse()

@router.get(
    "/list",
    summary="Список пользователей",
    response_model=AppResponse[UserDataListView]
)
async def get_list(
        pagination: RequestQueryPaginate,
        query: str = Query('', description="Поиск по имени")):
    data =  await UserService.get_list(
            query=query,
            pagination=pagination)
 
    return AppResponse[UserDataListView](
            data=data
        )