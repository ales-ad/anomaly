from typing import Optional
import datetime as dt

from fastapi import APIRouter, Query, Depends

from core.auth import admin_access, AuthUser


from core.response import AppResponse
from core.pagination import RequestQueryPaginate

from .request_models import (
        DictionatiesView
    )
from .service import DictionariesService




router = APIRouter(prefix="/dictionaries", tags=["dictionaries"])

@router.get(
    "/all",
    summary="Список",
    response_model=AppResponse[DictionatiesView]
)
async def get_data():
    return AppResponse[DictionatiesView](
        data=await DictionariesService.get_list()
    )

