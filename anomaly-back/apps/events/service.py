from typing import Optional
import datetime as dt
from itertools import cycle

from tortoise.transactions import in_transaction


from core import db
from core.logger import log
from core.pagination import RequestPaginate
from .models import Events, StatusEvents
from apps.users.models import User
from apps.clients.models import ClientGroups, Client, ClientIncome, StatusClient, ClientRole
from apps.cities.models import City
from .request_models import EventsListView, EventResponse, EventFullResponse, EventUpdatePatchRequest
from .exceptions import EventsNotFoundErr



class EventsService:
    
    @staticmethod
    def split_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i+chunk_size]
            
    @staticmethod
    async def reset(event_id:int):
        async with in_transaction() as con:
                await Client.filter(
                                event_id=event_id,
                            ).using_db(con).update(
                                groups_id=None,
                                link=None,
                                status=StatusClient.new
                            )
                await ClientGroups.filter(
                                event_id=event_id,
                            ).using_db(con).delete()
                
                await Events.filter(
                    id=event_id,
                    deleted_at=None
                ).using_db(con).update(status=StatusEvents.wait)
                            
    @staticmethod
    async def generate(event_id:int):
        chunk_size = 10
        group_number = 1

        min_group_size = 3

        args_groups = {}
        args_groups['event_id'] = event_id  
                            
        sql_groups = f"""
                                SELECT g.* 
                                FROM {ClientGroups.Meta.table} g
                                LEFT JOIN {Client.Meta.table} c on g.id=c.groups_id
                                WHERE  g.event_id=:event_id AND c.role_id=ANY(:role_id)
                                GROUP BY g.id
                            """
        
        async with in_transaction() as con:
            args = {}
            args['event_id'] = event_id

            row_with_leader = await Client.filter(
                event_id=event_id,
                is_leader=True
            ).using_db(con).all()
            count = len(row_with_leader)
            if count > 0:
                    log.info(f"[generate] is row_with_leader={count}")
           
            for item in row_with_leader:
                if item.role_id == 1:
                      args['role_id'] = [1]
                else:
                    args['role_id'] = [2,3]
                args['specialty_id'] = item.specialty_id
                args['income_id'] = item.income_id
                args['limit'] = 10 - item.count_group_current
      
                sql = f"""
                        (
                            SELECT 
                                c.id, c.income_id, c.groups_id, c.specialty_id , c.role_id ,c.is_leader, '0' as _sort_income
                            FROM clients c
                            LEFT JOIN client_income inc on  inc.id = c.income_id
                            WHERE 
                                c.role_id=ANY(:role_id) and c.event_id=:event_id and c.is_leader is False and c.groups_id is null and c.specialty_id = :specialty_id  and c.income_id = :income_id  
                            ORDER BY 
                                inc.from_value DESC, c.specialty_id ASC
                        )	
                        UNION ALL
                        (
                            SELECT 
                                c.id, c.income_id, c.groups_id, c.specialty_id , c.role_id ,c.is_leader,
                                CASE 
                                    WHEN c.income_id = :income_id THEN 1
                                    WHEN c.income_id > :income_id THEN 2
                                    else  3
                                END AS _sort_income
                            FROM clients c
                            WHERE 
                                c.role_id=ANY(:role_id) and c.event_id=:event_id and c.is_leader is False and c.groups_id is null and not (c.specialty_id = :specialty_id  and c.income_id = :income_id  ) 
                            ORDER BY  _sort_income ASC
                        )

                        LIMIT :limit

                    """
                log.info(f"[generate] sql={sql}")
                rows_leader= await con.execute_query_dict(*db.sql(sql, **args))
                if rows_leader:
                    log.info(f"[generate] {args} rows_leader={rows_leader}")
                    grLeader = ClientGroups(
                                    number=group_number,
                                    event_id=event_id,
                                )
                    await grLeader.save(using_db=con)
                    group_number = group_number + 1
                    item.groups_id = grLeader.id
                    await item.save(using_db=con)
                    for rowClient in rows_leader:
                        await Client.filter(
                                id=rowClient['id'],
                            ).using_db(con).update(
                                groups_id=grLeader.id
                            )

          
            # фомируем десятки
            args['role_id'] = [2,3]
            sql = f"""
                SELECT c.* 
                FROM {Client.Meta.table} c
                LEFT JOIN {ClientIncome.Meta.table} inc on  inc.id = c.income_id
                WHERE 
                    c.role_id=ANY(:role_id) and c.event_id=:event_id and c.groups_id is null 
                ORDER BY 
                    inc.from_value DESC, c.specialty_id ASC
            """
             # НЕ предприниматели
            rows = await con.execute_query_dict(*db.sql(sql, **args))
            if rows:
                gr = None
                for chunk in EventsService.split_list(rows, chunk_size):
                    print("chunk count not bissnes", len(chunk))

                    if len(chunk)<min_group_size:
                            args_groups['role_id'] = [2,3]   
                            rows_groups = await con.execute_query_dict(*db.sql(sql_groups, **args_groups))
                            if rows_groups:
                                pool = cycle(rows_groups)
                                for item in chunk:
                                        gr_current = next(pool)
                                        await Client.filter(
                                                id=item['id'],
                                        ).using_db(con).update(groups_id=gr_current['id'])
                                continue;
                    
                    gr = ClientGroups(
                                    number=group_number,
                                    event_id=event_id,
                            )
                    await gr.save(using_db=con)

                    for item in chunk:
                         await Client.filter(
                                id=item['id'],
                            ).using_db(con).update(
                                groups_id=gr.id
                            )
                    group_number = group_number + 1

            # предприниматели
            args['role_id'] = [1]    
            rows_ = await con.execute_query_dict(*db.sql(sql, **args))
            if rows_:
                grBis = None
                for chunk in EventsService.split_list(rows_, chunk_size):
                    print("chunk count bissnes", len(chunk))
  
                    if len(chunk)<min_group_size:
                            args_groups['role_id'] = [1]   
                            rows_groups = await con.execute_query_dict(*db.sql(sql_groups, **args_groups))
                            if rows_groups:
                                pool = cycle(rows_groups)
                                for item in chunk:
                                        gr_current = next(pool)
                                        await Client.filter(
                                                id=item['id'],
                                        ).using_db(con).update(groups_id=gr_current['id'])
                                continue;
                                              
                  
                    grBis = ClientGroups(
                                    number=group_number,
                                    event_id=event_id,
                    )
                    await grBis.save(using_db=con)
                        
                    for item in chunk:
                            await Client.filter(
                                    id=item['id'],
                            ).using_db(con).update(groups_id=grBis.id)
                    group_number = group_number + 1
                            
            await Events.filter(
                id=event_id,
                deleted_at=None
            ).using_db(con).update(status=StatusEvents.generated)
            
    @staticmethod
    async def get_list(
            query: str,
            pagination: RequestPaginate,
            date: Optional[dt.date] = None,
            moderator_id: Optional[int] = None,
    ) -> EventsListView:
        
        args = {}
        filters = ' e.deleted_at is NULL '
        async with in_transaction() as con:

            if query:
                    args['query_arg'] = query
                    filters += " AND  (lower(e.name) LIKE lower(concat('%', :query_arg::varchar, '%'))  OR  lower(c.name) LIKE lower(concat('%', :query_arg::varchar, '%')))"
            if date is not None:
                    filters += ' AND e.date = :date '
                    args['date'] = date
            if moderator_id is not None:
                    filters += ' AND e.moderator_id = :moderator_id '
                    args['moderator_id'] = moderator_id


            if (pagination is not None) and (not pagination.full):
                limit_query = ' LIMIT :limit OFFSET :offset '
                args['limit'] = pagination.limit
                args['offset'] = pagination.offset
            else:
                limit_query = ''

            sql = f"""
                SELECT
                    e.*,
                    c.name as city_name,
                    u.login as moderator_name,

                    COUNT(*) OVER () AS total_count
                FROM 
                    {Events.Meta.table} e
                        INNER JOIN {City.Meta.table} c ON c.id = e.city_id
                        INNER JOIN {User.Meta.table} u ON u.id = e.moderator_id
                    WHERE {filters}
       
                ORDER BY id DESC
                {limit_query}
            """

            rows = await con.execute_query_dict(*db.sql(sql, **args))

            if not rows:
                return EventsListView(items=[],total=0)
            else:
                return EventsListView(
                    items=[
                        EventFullResponse.model_validate(r,context={'from': 'SQL'})
                        for r in rows
                    ],
                    total=rows[0]['total_count']
                )

    @staticmethod
    async def update(
            id: int,
            city_id: int,
            moderator_id: int,
            name: str,
            date: dt.date,
    ) -> EventResponse:
        async with in_transaction() as con:
            ev = await Events.filter(
                id=id,
                deleted_at=None
            ).using_db(con).update(
                name=name,
                date=date,
                moderator_id=moderator_id,
                city_id=city_id,
            )
            
            if ev == 0:
                raise EventsNotFoundErr
            
            ev = await Events.filter(
                id=id,
            ).using_db(con).first()
            return EventResponse.model_validate(ev, from_attributes=True)
    
    @staticmethod    
    async def patch(
            id: int,
            data: EventUpdatePatchRequest,
    ):
        async with in_transaction() as con:
            cl_data = data.model_dump(exclude_unset=True)
            ev = await Events.filter(
                id=id,
            ).using_db(con).update(**cl_data)

        
            if ev == 0:
                raise EventsNotFoundErr
            
            ev = await Events.filter(
                id=id,
            ).using_db(con).first()

            return EventResponse.model_validate(ev, from_attributes=True)

    @staticmethod
    async def create(
            city_id: int,
            moderator_id: int,
            name: str,
            date: dt.date,
    ) -> EventResponse:

         async with in_transaction() as con:
            ev = Events(
                name=name,
                date=date,
                moderator_id=moderator_id,
                city_id=city_id,
            )
            await ev.save(using_db=con)

            return EventResponse.model_validate(ev, from_attributes=True)

    @staticmethod
    async def delete(
            id: int,
    ):
        async with in_transaction() as con:
            usr = await Events.filter(
                    id=id,
                    deleted_at=None
                ).using_db(con).update(deleted_at=dt.datetime.now()) 

            if not usr:
                raise EventsNotFoundErr
            
    @staticmethod
    async def detail(
            event_id: int,

    ) -> EventResponse:

        async with in_transaction() as con:
            usr = await Events.filter(
                    id=event_id
                ).using_db(con).prefetch_related('city').using_db(con).first()    

            if not usr:
                raise EventsNotFoundErr
           
            data = EventResponse.model_validate(usr, from_attributes=True)
            data.city_name = usr.city.name if usr.city else None
            return data