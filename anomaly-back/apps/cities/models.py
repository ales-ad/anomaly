from tortoise import Model, fields


class City(Model):
    class Meta:
        table = "cities"

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=31, null=True)
    deleted_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
