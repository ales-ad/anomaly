
import datetime
from passlib.context import CryptContext

from tortoise.transactions import in_transaction



from core import db
from core.pagination import RequestPaginate
from ..models import User, RoleEnum
from ..request_models import UserDataRequest, UserDataListView, UserUpdatePatchRequest
from ..exceptions import UserNotFoundErr


class UserService:

    @staticmethod
    async def get_list(
            query: str,
            pagination: RequestPaginate
    ) -> UserDataListView:
        
        args = {}
        async with in_transaction() as con:
            query_condition = ""

            if query:
                    args['query_arg'] = query
                    query_condition = " WHERE  lower(u.login) LIKE lower(concat('%', :query_arg::varchar, '%'))"

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
                    {User.Meta.table} u
                
                    {query_condition if query else ' '}
                ORDER BY id DESC
                {limit_query}
            """

            rows = await con.execute_query_dict(*db.sql(sql, **args))

            if not rows:
                raise UserNotFoundErr
            else:
                return UserDataListView(
                    items=[
                        UserDataRequest.model_validate(r)
                        for r in rows
                    ],
                    total=rows[0]['total_count']
                )
    
    @staticmethod
    async def delete(
            id: int,
    ):
        async with in_transaction() as con:
            usr = await User.filter(
                    id=id,
                    deleted_at=None
                ).using_db(con).update(deleted_at=datetime.datetime.now()) 

            if not usr:
                raise UserNotFoundErr

        
    @staticmethod
    async def detail(
            id: int,
    ) -> UserDataRequest:
        async with in_transaction() as con:
            usr = await User.filter(
                    id=id
                ).using_db(con).first()   

            if not usr:
                raise UserNotFoundErr
            return UserDataRequest.model_validate(usr, from_attributes=True)
    
    @staticmethod
    async def create(
            login: str,
            password: str,
            role: RoleEnum,
    ) -> int:
         pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
         async with in_transaction() as con:
            mp = User(
                login=login,
                role=role,
                password=pwd_context.hash(password)
            )
            await mp.save(using_db=con)

    @staticmethod
    async def update(
            id: int,
            login: int,
            role: RoleEnum
    ):
        async with in_transaction() as con:
            ev = await User.filter(
                id=id,
            ).using_db(con).update(
                login=login,
                role=role,
            )
            
            if ev == 0:
                raise UserNotFoundErr

    @staticmethod
    async def patch(
            id: int,
            data: UserUpdatePatchRequest,
    ):
        async with in_transaction() as con:
            cl_data = data.model_dump(exclude_unset=True)
            if (data.password):
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                cl_data["password"]=pwd_context.hash(data.password)
                
            ev = await User.filter(
                id=id,
            ).using_db(con).update(**cl_data)

            

            if ev == 0:
                raise UserNotFoundErr

          