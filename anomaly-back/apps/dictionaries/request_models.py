import datetime as dt
from pydantic import BaseModel

class RoleData(BaseModel):
    id: int
    name: str
  
   
class IncomeData(BaseModel):
    id: int
    name: str

class SpecialtyData(BaseModel):
    id: int
    name: str

class DictionatiesView(BaseModel):
    role:list[RoleData]
    income:list[IncomeData]
    specialty:list[SpecialtyData]
