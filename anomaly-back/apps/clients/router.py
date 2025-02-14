from typing import Optional
import datetime as dt

from fastapi import APIRouter, Query, Depends

from core.auth import admin_access, AuthUser


from core.response import AppResponse
from core.pagination import RequestQueryPaginate

from .request_models import (
    ClientResponse,
    ClientCreateRequest,
    ClientUpdateRequest,
    ClientView
    )
from .service import ClientService




router = APIRouter(prefix="/clients", tags=["clients"])

@router.post(
    "",
    summary="Создание",
    response_model=AppResponse[ClientResponse]
)
async def create_client(req: ClientCreateRequest):
    return AppResponse[ClientResponse](
        data=await ClientService.create(data=req)
    )

@router.get(
    "/list",
    summary="Список ",
    response_model=AppResponse[ClientView],
)
async def get_list_event(
        pagination: RequestQueryPaginate,
        group_id: Optional[int] = Query(None, description="ИД группы"),
        event_id: Optional[int] = Query(None, description="ИД События"),
        ):
    
        data =  await ClientService.get_list(
            pagination=pagination,
            group_id=group_id,
            event_id=event_id,
            )
 
        return AppResponse[ClientView](
                data=data
            )
        
@router.get(
    "/get-by-tg/{tg_id}/{event_id}",
    summary="Данные по TG ID",
    response_model=AppResponse()
)
async def update_client(tg_id:int,event_id:int):
    return AppResponse(
        data=await ClientService.detailByTg(tg_id,event_id)
    )
    
@router.patch(
    "/get-by-tg/{tg_id}/{event_id}",
    summary="Данные",
    response_model=AppResponse()
)
async def update_client(tg_id:int,event_id:int, req: ClientUpdateRequest):
    return AppResponse(
        data=await ClientService.updateByTg(tg_id=tg_id,event_id=event_id, data=req)
    )
    
@router.get(
    "/{client_id}",
    summary="Данные",
    response_model=AppResponse()
)
async def update_client(client_id:int):
    return AppResponse(
        data=await ClientService.detail(client_id)
    )

@router.put(
    "/{client_id}",
    summary="Изменение",
    response_model=AppResponse[ClientResponse]
)
async def update_client(client_id: int, req: ClientUpdateRequest):
    return AppResponse[ClientResponse](
        data=await ClientService.update(id=client_id, data=req, mode='put')
    )

@router.patch(
    "/{client_id}",
    summary="Изменение",
    response_model=AppResponse[ClientResponse]
)
async def patch_client(client_id: int, req: ClientUpdateRequest):
    return AppResponse[ClientResponse](
        data=await ClientService.update(id=client_id, data=req, mode='patch')
    )


