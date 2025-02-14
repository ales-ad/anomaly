from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field


class RequestPaginate(BaseModel):
    limit: int = Field(20, description="Макс. количество записей", gt=0)
    offset: int = Field(0, description="Смещение относительно первой записи", ge=0)
    full: bool = Field(
        False,
        description="Если включено, limit и offset игнорируются",
        alias='_full'
    )


class OptionalRequestPaginate(RequestPaginate):
    full: bool = Field(
        True,
        description="Если включено, limit и offset игнорируются",
        alias='_full'
    )


RequestQueryPaginate = Annotated[RequestPaginate, Depends()]
OptionalRequestQueryPaginate = Annotated[OptionalRequestPaginate, Depends()]

RequestBodyPaginate = RequestPaginate


def local_paginate(
        items: list,
        pagination: RequestPaginate
) -> list:
    if not pagination.full:
        _li = min(pagination.offset, len(items))
        _ri = min(_li + pagination.limit, len(items))

        return items[_li:_ri]
    else:
        return items
