from typing import Optional
import datetime as dt

from fastapi import APIRouter, Query

from core.response import AppResponse

from apps.clients.request_models import (
    groupsListView
    )
from .service import GroupsService


router = APIRouter(prefix="/groups", tags=["groups"])


@router.get(
    "/list",
    summary="Список ",
    response_model=AppResponse[groupsListView],
)
async def get_list_group(
        event_id: Optional[int] = Query(None, description="Отфильтровать по дате "),
        ):
    
        data =  await GroupsService.get_list(
            event_id=event_id
            )
 
        return AppResponse[groupsListView](
                data=data
            )




