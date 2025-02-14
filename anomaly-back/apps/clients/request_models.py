import datetime as dt
from pydantic import BaseModel
from typing import Optional

class groupsView(BaseModel):
    number:  Optional[int] = None 
    event_id:  Optional[int] = None 
    id:  Optional[int] = None 


class groupsListView(BaseModel):
    items: Optional[list[groupsView]] = None
    total: int

class ClientResponse(BaseModel):
    id: int
    tg_id: Optional[str] = None 
    tg_username: Optional[str] = None 
    name: str
    age: int
    link: Optional[str] = None 
    specialty_id: int
    income_id: int
    role_id: int
    event_id: int
    is_leader: bool
    count_group_current: int
    groups_id: Optional[int] = None 
    status: Optional[str]  
    groups_number: Optional[int] = None 
    #groups:Optional[groupsView] = None 


class ClientFullResponse(ClientResponse):
    specialty_name: Optional[str] = None 
    income_name: Optional[str] = None 
    role_name: Optional[str] = None 
    city: Optional[str] = None 

class ClientView(BaseModel):
    items: Optional[list[ClientFullResponse]] = None
    total: int

class ClientCreateRequest(BaseModel):
    tg_id: Optional[str] = None 
    tg_username:  Optional[str] = None 
    name:  str  
    age:  Optional[int] = None 
    link:  Optional[str] = None 
    specialty_id:  Optional[int] = None 
    income_id:  Optional[int] = None 
    role_id:  Optional[int] = None 
    is_leader: bool 
    count_group_current: int
    event_id: int

class ClientUpdateRequest(BaseModel):
    tg_id: Optional[str] = None 
    tg_username:  Optional[str] = None 
    name:  Optional[str] = None  
    age:  Optional[int] = None 
    link:  Optional[str] = None 
    specialty_id:  Optional[int] = None 
    income_id:  Optional[int] = None 
    role_id:  Optional[int] = None 
    groups_id: Optional[int] = None 
    status: Optional[str] = None 
    is_leader:  Optional[bool ] = False
    count_group_current:  Optional[int] = 0
   
