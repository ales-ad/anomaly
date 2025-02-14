import datetime as dt
from pydantic import BaseModel
from typing import Optional
from .models import StatusEvents

class EventCreateRequest(BaseModel):
    name: str
    city_id: int
    moderator_id: int
    date: dt.date
   
class EventUpdateRequest(BaseModel):
    name: str
    city_id: int
    moderator_id: int
    date: dt.date
    status: Optional[StatusEvents]


class EventUpdatePatchRequest(BaseModel):
    name: Optional[str] = None
    city_id: Optional[int] = None
    moderator_id: Optional[int] = None
    date: Optional[dt.date] = None
    status: Optional[StatusEvents] = None


class EventResponse(BaseModel):
    id: int
    name: str
    city_id: int
    city_name: Optional[str] = None
    moderator_id: int
    date: dt.date
    status: StatusEvents
    
class EventFullResponse(BaseModel):
    id: int
    name: str
    city_id: int
    moderator_id: int
    city_name: str
    moderator_name: str
    status: StatusEvents
    date: dt.date

class EventsListView(BaseModel):
    items: Optional[list[EventFullResponse]] = None
    total: int