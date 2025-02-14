from tortoise import Model, fields
from enum import Enum


class StatusEvents(str, Enum):
    wait = 'wait'
    start = 'start'
    generated = 'generated'

class Events(Model):
    class Meta:
        table = "events"

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=31, null=True)
    city = fields.ForeignKeyField("models.City", on_delete=fields.NO_ACTION, null=False)
    moderator = fields.ForeignKeyField("models.User", on_delete=fields.NO_ACTION, null=True)
    date = fields.DateField(null=True)
    status = fields.CharEnumField(enum_type=StatusEvents,  null=False, default=StatusEvents.wait)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
