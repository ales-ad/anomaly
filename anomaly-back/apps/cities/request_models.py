from pydantic import BaseModel
from typing import Optional

class CityCreateRequest(BaseModel):
    name: str
   
class CityUpdateRequest(BaseModel):
    name: str

class CityRequest(BaseModel):
    id: int
    name: str

class CitiesListView(BaseModel):
    items: Optional[list[CityRequest]] = None
    total: int