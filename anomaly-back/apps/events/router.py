from typing import Optional
import datetime as dt

from fastapi import APIRouter, Query, Depends

from core.auth import admin_access, AuthUser

from apps.users.models import RoleEnum
from core.response import AppResponse
from core.pagination import RequestQueryPaginate

from .request_models import (
    EventResponse,
    EventCreateRequest,
    EventsListView,
    EventUpdateRequest,
    EventUpdatePatchRequest
    )
from .service import EventsService




router = APIRouter(prefix="/events", tags=["events"])

@router.post(
    "",
    summary="Создание",
    response_model=AppResponse[EventResponse]
)
async def create_event(req: EventCreateRequest):
    return AppResponse[EventResponse](
        data=await EventsService.create(name=req.name,city_id=req.city_id, moderator_id=req.moderator_id, date=req.date)
    )
    
@router.post(
    "/create-group/{event_id}",
    summary="Создание десяток",
    response_model=AppResponse()
)
async def create_group(event_id:int):

    await EventsService.generate(event_id)   
    return AppResponse()

@router.post(
    "/reset-group/{event_id}",
    summary="Сброс десяток",
    response_model=AppResponse()
)
async def create_group(event_id:int):

    await EventsService.reset(event_id)   
    return AppResponse()

@router.get(
    "/list",
    summary="Список ",
    response_model=AppResponse[EventsListView],
    dependencies=[Depends(admin_access)],
)
async def get_list_event(
        pagination: RequestQueryPaginate,
        user: AuthUser = Depends(admin_access),
        query: str = Query('', description="Поиск по наименованию"),
        date: Optional[dt.date] = Query(None, description="Отфильтровать по дате "),
        ):
    
        data =  await EventsService.get_list(
            query=query,
            pagination=pagination,
            date=date,
            moderator_id=user.id if user.role==RoleEnum.moderator else None
            )
 
        return AppResponse[EventsListView](
                data=data
            )

@router.get(
    "/{event_id}",
    summary="Детали",
    response_model=AppResponse[EventResponse]
)
async def get_event(event_id:int):
    return AppResponse[EventResponse](
        data=await EventsService.detail(event_id)
    )


@router.put(
    "/{event_id}",
    summary="Изменение",
    response_model=AppResponse[EventResponse]
)
async def update_event(event_id: int, req: EventUpdateRequest):
    return AppResponse[EventResponse](
        data=await EventsService.update(id=event_id,name=req.name, city_id=req.city_id, moderator_id=req.moderator_id, date=req.date)
    )

@router.patch(
    "/{event_id}",
    summary="Изменение",
    response_model=AppResponse[EventResponse]
)
async def update_event(event_id: int, req: EventUpdatePatchRequest):
    return AppResponse[EventResponse](
        data=await EventsService.patch(id=event_id,data=req)
    )


@router.delete(
    "/{event_id}",
    summary="Удаление ",
    response_model=AppResponse
)
async def delete_event(event_id: int):
    await EventsService.delete(event_id)
 
    return AppResponse()

