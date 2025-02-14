from typing import Optional
import datetime as dt

from tortoise.transactions import in_transaction


from core import db
from core.pagination import RequestPaginate
from apps.clients.models import ClientIncome, ClientRole, ClientSpecialty

from .request_models import (
        DictionatiesView,
        RoleData,
        IncomeData,
        SpecialtyData
    )


class DictionariesService:


    @staticmethod
    async def get_list(
          
    ) -> DictionatiesView:
        async with in_transaction() as con:
            client_role = await ClientRole.all().order_by('id').using_db(con)
            client_income = await ClientIncome.all().order_by('from_value').using_db(con)
            client_specialty =await  ClientSpecialty.all().order_by('id').using_db(con)

         
            return DictionatiesView(
                        role=[
                            RoleData.model_validate(r, from_attributes=True)
                            for r in client_role
                        ],
                        specialty=[
                            SpecialtyData.model_validate(r, from_attributes=True)
                            for r in client_specialty
                        ],
                        income=[
                            IncomeData.model_validate(r, from_attributes=True)
                            for r in client_income
                        ],
                    )

