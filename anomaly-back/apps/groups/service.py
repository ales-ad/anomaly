from typing import Optional, Literal

from tortoise.transactions import in_transaction

from core import db
from apps.clients.models import  ClientGroups

from apps.clients.request_models import (
    groupsView,
    groupsListView
    )


class GroupsService:
    @staticmethod
    async def get_list(
            event_id: Optional[int] = None,
    ) -> groupsListView:
        args = {}
        filters = ' TRUE '
        async with in_transaction() as con:

            if event_id is not None:
                    filters += ' AND g.event_id = :event_id '
                    args['event_id'] = event_id

            sql = f"""
                SELECT
                    g.*,
                    COUNT(*) OVER () AS total_count
                FROM 
                    {ClientGroups.Meta.table} g
                    WHERE {filters}
                ORDER BY number DESC
            """

            rows = await con.execute_query_dict(*db.sql(sql, **args))

            if not rows:
                return groupsListView(items=[],total=0)
            else:
                return groupsListView(
                    items=[
                        groupsView.model_validate(r,context={'from': 'SQL'})
                        for r in rows
                    ],
                    total=rows[0]['total_count']
                )
        return None
