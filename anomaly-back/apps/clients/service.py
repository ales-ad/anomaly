from typing import Optional, Literal


from tortoise.transactions import in_transaction


from core import db
from core.pagination import RequestPaginate
from apps.clients.models import ClientIncome, ClientRole, ClientSpecialty, ClientGroups, Client
from apps.cities.models import City
from apps.events.models import Events

from .request_models import (
    ClientResponse,
    ClientCreateRequest,
    ClientUpdateRequest,
    ClientView,
    ClientFullResponse
    )

class ClientService:
    
    @staticmethod
    async def get_list(
            pagination: RequestPaginate,
            group_id: Optional[int] = None,
            event_id: Optional[int] = None
    ) -> ClientView:
        args = {}
        filters = ' TRUE '
        async with in_transaction() as con:

   
            if group_id is not None:
                    filters += ' AND e.groups_id = :group_id '
                    args['group_id'] = group_id
            if event_id is not None:
                    filters += ' AND e.event_id = :event_id '
                    args['event_id'] = event_id

            if (pagination is not None) and (not pagination.full):
                limit_query = ' LIMIT :limit OFFSET :offset '
                args['limit'] = pagination.limit
                args['offset'] = pagination.offset
            else:
                limit_query = ''

            sql = f"""
                SELECT
                    e.*,
                    c.number as groups_number,
                    inc.name as income_name,
                    rl.name as role_name,
                    sp.name as specialty_name,
                    ci.name as city,
                    COUNT(*) OVER () AS total_count
                FROM 
                    {Client.Meta.table} e
                        LEFT JOIN {ClientGroups.Meta.table} c ON c.id = e.groups_id
                         LEFT JOIN {ClientIncome.Meta.table} inc ON inc.id = e.income_id
                         LEFT JOIN {ClientRole.Meta.table} rl ON rl.id = e.role_id
                         LEFT JOIN {ClientSpecialty.Meta.table} sp ON sp.id = e.specialty_id
                         LEFT JOIN {Events.Meta.table} ev ON ev.id = e.event_id
                         LEFT JOIN {City.Meta.table} ci ON ci.id = ev.city_id
            
                    WHERE {filters}
       
                ORDER BY e.groups_id ASC, e.id DESC
                {limit_query}
            """

            rows = await con.execute_query_dict(*db.sql(sql, **args))

            if not rows:
                return ClientView(items=[],total=0)
            else:
                return ClientView(
                    items=[
                        ClientFullResponse.model_validate(r,context={'from': 'SQL'})
                        for r in rows
                    ],
                    total=rows[0]['total_count']
                )
        return None

    @staticmethod
    async def detail(
            client_id: int
    ) -> ClientResponse:
        async with in_transaction() as con:
            usr = await Client.filter(
                    id=client_id
                ).prefetch_related('groups').using_db(con).first()   

            if not usr:
                return None
           
            data = ClientResponse.model_validate(usr, from_attributes=True)
            data.groups_number = usr.groups.number if usr.groups else None

            return data
        
    @staticmethod
    async def detailByTg(
            tg_id: int,
            event_id: int
    ) -> ClientResponse:
        async with in_transaction() as con:
            usr = await Client.filter(
                    tg_id=tg_id,
                    event_id=event_id,
                ).prefetch_related('groups').using_db(con).first()   

            if not usr:
                return None
           
            data = ClientResponse.model_validate(usr, from_attributes=True)
            data.groups_number = usr.groups.number if usr.groups else None

            return data

    @staticmethod
    async def create(
            data: ClientCreateRequest
    ) -> ClientResponse:
         async with in_transaction() as con:
            cl_data = data.model_dump(exclude_unset=True)
            
            ev = Client(**cl_data)
            await ev.save(using_db=con)
            return ClientResponse.model_validate(ev, from_attributes=True)

    @staticmethod
    async def update(
            id: int,
            data: ClientUpdateRequest,
            mode: Literal['patch', 'put'] = 'put'
    ) -> ClientResponse:
        async with in_transaction() as con:
            if mode == 'put':
                cl_data = data.model_dump()
            else:
                cl_data = data.model_dump(exclude_unset=True)

            ev = await Client.filter(
                id=id,
            ).using_db(con).update(
                **cl_data
            )
            
            ev = await Client.filter(
                id=id,
            ).using_db(con).first()
            return ClientResponse.model_validate(ev, from_attributes=True)
        
    @staticmethod
    async def updateByTg(
            tg_id: int,
            event_id: int,
            data: ClientUpdateRequest
    ) -> ClientResponse:
        async with in_transaction() as con:
            cl_data = data.model_dump(exclude_unset=True)

            ev = await Client.filter(
                tg_id=tg_id,
                event_id=event_id
            ).using_db(con).update(
                **cl_data
            )
            
            ev = await Client.filter(
                tg_id=tg_id,
                event_id=event_id
            ).using_db(con).first()
            return ClientResponse.model_validate(ev, from_attributes=True)