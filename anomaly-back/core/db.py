import os
import re
import ssl

from tortoise.backends.asyncpg.client import AsyncpgDBClient
from tortoise import connections

from config import config

from core.logger import log


models = []
for obj in os.scandir("apps"):
    if obj.is_dir():
        if os.path.isfile(f"apps/{obj.name}/models.py"):
            models.append(f"apps.{obj.name}.models")

ssl_cont = None
if config.DB.sslmode != "disable":
    ssl_cont = ssl.create_default_context()
    # ssl_cont.verify_mode = ssl.VerifyMode.CERT_NONE

TORTOISE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": config.DB.db_name,
                "host": config.DB.host,
                "password": config.DB.password,
                "port": config.DB.port,
                "user": config.DB.user,
                "ssl": ssl_cont
            }
        }
    },
    "apps": {
        "models": {
            "models": [*models, "aerich.models"],
            "default_connection": "default"
        }
    },
    "use_tz": True,
    "timezone": "UTC"
}


def sql(sql_text: str, **params):
    db_args = []
    i = 0

    for key, value in params.items():
        template = fr":{key}\b"
        index = re.search(template, sql_text)
        if index is not None:
            i += 1
            db_args.append(value)

        sql_text = re.sub(template, f"${i}", sql_text)

    return sql_text, db_args


Connection = AsyncpgDBClient


class Transaction:
    def __init__(self):
        self.trx = None

    async def __aenter__(self):
        log.info("Enter in transaction")
        con: Connection = await get_connection()  # noqa
        self.trx = con._in_transaction()
        return await self.trx.__aenter__()

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        log.info("Exit out of transaction")
        return await self.trx.__aexit__(exc_type, exc_value, exc_tb)


async def get_connection() -> Connection:
    # default - не имя коннекции, а имя грубо говоря их пула
    return connections.get('default')
