from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

from core.request import AppRequest

DataType = TypeVar("DataType")


def _get_req_id():
    return AppRequest.id


class Error(BaseModel):
    name: str
    extra_info: dict | None = None


class AppResponse(BaseModel, Generic[DataType]):
    req_id: str = Field(..., default_factory=_get_req_id)
    resp_datetime: datetime = Field(..., default_factory=datetime.utcnow)
    error: Error | None = None
    data: DataType | None = None
