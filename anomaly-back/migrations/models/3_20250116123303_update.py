from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "events" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(31),
    "date" DATE,
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "city_id" BIGINT NOT NULL REFERENCES "cities" ("id") ON DELETE NO ACTION,
    "moderator_id" BIGINT REFERENCES "users" ("id") ON DELETE NO ACTION
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "events";"""
