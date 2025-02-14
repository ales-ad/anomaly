import datetime

from tortoise.transactions import in_transaction



from core import db
from core.pagination import RequestPaginate
from .models import City
from .request_models import CitiesListView, CityRequest
from .exceptions import CityNotFoundErr



class CityService:

    @staticmethod
    async def get_list(
            query: str,
            pagination: RequestPaginate
    ) -> CitiesListView:
        
        args = {}
        async with in_transaction() as con:
            query_condition = ""

            if query:
                    args['query_arg'] = query
                    query_condition = "   lower(u.name) LIKE lower(concat('%', :query_arg::varchar, '%'))"

            if (pagination is not None) and (not pagination.full):
                limit_query = ' LIMIT :limit OFFSET :offset '
                args['limit'] = pagination.limit
                args['offset'] = pagination.offset
            else:
                limit_query = ''

            sql = f"""
                SELECT
                    *,
                    COUNT(*) OVER () AS total_count
                FROM
                    {City.Meta.table} u
                    WHERE deleted_at is NULL
                    {query_condition if query else ' '}
                ORDER BY id DESC
                {limit_query}
            """

            rows = await con.execute_query_dict(*db.sql(sql, **args))

            if not rows:
                return CitiesListView(
                    items=[],total=0)
            else:
                return CitiesListView(
                    items=[
                        CityRequest.model_validate(r)
                        for r in rows
                    ],
                    total=rows[0]['total_count']
                )

    @staticmethod
    async def update(
            city_id: int,
            name: str,
    ) -> CityRequest:
        async with in_transaction() as con:
            city = await City.filter(
                id=city_id,
            ).using_db(con).update(
                name=name,
                deleted_at=None
            )
            
            if city == 0:
                raise CityNotFoundErr
            
            city = await City.filter(
                id=city_id,
            ).using_db(con).first()
            return CityRequest.model_validate(city, from_attributes=True)

    @staticmethod
    async def create(
            name: str,
    ) -> int:

         async with in_transaction() as con:
            city = City(
                name=name,
            )
            await city.save(using_db=con)

            return CityRequest.model_validate(city, from_attributes=True)

    @staticmethod
    async def delete(
            id: int,
    ):
        async with in_transaction() as con:
            usr = await City.filter(
                    id=id,
                    deleted_at=None
                ).using_db(con).update(deleted_at=datetime.datetime.now()) 

            if not usr:
                raise CityNotFoundErr