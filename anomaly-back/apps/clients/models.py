from tortoise import Model, fields
from enum import Enum


class StatusClient(str, Enum):
    new = 'new'
    completed = 'completed'


class ClientGroups(Model):
    class Meta:
        table = "client_groups"

    id = fields.BigIntField(pk=True)
    number = fields.IntField(max_length=100, null=True)
    event = fields.ForeignKeyField("models.Events", on_delete=fields.NO_ACTION, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

class ClientSpecialty(Model):
    class Meta:
        table = "client_specialty"

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class ClientRole(Model):
    class Meta:
        table = "client_role"

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class ClientIncome(Model):
    class Meta:
        table = "client_income"

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    from_value = fields.IntField(max_length=100, null=True)
    to_value = fields.IntField(max_length=100, null=True)
    name = fields.CharField(max_length=100, null=True)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class ClientToIncome(Model):
    class Meta:
        table = "client_to_income"

    id = fields.BigIntField(pk=True)
    income = fields.ForeignKeyField("models.ClientIncome",  on_delete=fields.NO_ACTION, null=False)
    client = fields.ForeignKeyField("models.Client", related_name="client_to_income", on_delete=fields.NO_ACTION, null=False)


class Client(Model):
    class Meta:
        table = "clients"

    id = fields.BigIntField(pk=True)
    tg_username = fields.CharField(max_length=100, null=True)
    tg_id = fields.CharField(max_length=100, null=True)

    name = fields.CharField(max_length=100, null=True)
    age = fields.IntField(max_length=3, null=True)
    link  = fields.CharField(max_length=200, null=True)

    specialty = fields.ForeignKeyField("models.ClientSpecialty", on_delete=fields.NO_ACTION, null=True)
    income = fields.ForeignKeyField("models.ClientIncome", on_delete=fields.NO_ACTION, null=True)
    role = fields.ForeignKeyField("models.ClientRole", on_delete=fields.NO_ACTION, null=True)
    event = fields.ForeignKeyField("models.Events", on_delete=fields.NO_ACTION, null=False)
    groups = fields.ForeignKeyField("models.ClientGroups", on_delete=fields.NO_ACTION, null=True)

    status = fields.CharEnumField(enum_type=StatusClient,  null=False, default=StatusClient.new)
    is_leader = fields.BooleanField(default=False)
    count_group_current = fields.IntField(max_length=3, null=False, default=0)
 
    created_at = fields.DatetimeField(auto_now_add=True)
