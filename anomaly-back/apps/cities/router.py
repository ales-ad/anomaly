from fastapi import APIRouter, Query


from core.response import AppResponse
from core.pagination import RequestQueryPaginate

from .request_models import (
    CitiesListView,
    CityCreateRequest,
    CityUpdateRequest,
    CityRequest
 
    )
from .service import CityService




router = APIRouter(prefix="/cities", tags=["cities"])

@router.post(
    "",
    summary="Создание",
    response_model=AppResponse[CityRequest]
)
async def create_city(req: CityCreateRequest):
    return AppResponse[CityRequest](
        data=await CityService.create(name=req.name)
    )


@router.put(
    "/{city_id}",
    summary="Изменение",
    response_model=AppResponse[CityRequest]
)
async def update_city(city_id: int, req: CityUpdateRequest):
    return AppResponse[CityRequest](
        data=await CityService.update(city_id=city_id,name=req.name)
    )


@router.delete(
    "/{city_id}",
    summary="Удаление ",
    response_model=AppResponse
)
async def delete_city(city_id: int):
    await CityService.delete(city_id)
 
    return AppResponse()

@router.get(
    "/list",
    summary="Список ",
    response_model=AppResponse[CitiesListView]
)
async def get_list_city(
        pagination: RequestQueryPaginate,
        query: str = Query('', description="Поиск по наименованию"),
        ):
    data =  await CityService.get_list(
            query=query,
            pagination=pagination)
 
    return AppResponse[CitiesListView](
            data=data
        )