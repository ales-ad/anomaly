from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
       
        CREATE TABLE IF NOT EXISTS "client_groups" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "number" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event_id" BIGINT NOT NULL REFERENCES "events" ("id") ON DELETE NO ACTION
);
        CREATE TABLE IF NOT EXISTS "client_income" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100),
    "from_value" INT,
    "to_value" INT,
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "client_role" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100),
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "client_specialty" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100),
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

 CREATE TABLE IF NOT EXISTS "clients" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tg_username" VARCHAR(100),
    "tg_id" VARCHAR(100),
    "name" VARCHAR(100),
    "age" INT,
    "link" VARCHAR(200),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event_id" BIGINT NOT NULL REFERENCES "events" ("id") ON DELETE NO ACTION,
    "groups_id" BIGINT REFERENCES "client_groups" ("id") ON DELETE NO ACTION,
    "income_id" BIGINT REFERENCES "client_income" ("id") ON DELETE NO ACTION,
    "role_id" BIGINT REFERENCES "client_role" ("id") ON DELETE NO ACTION,
    "specialty_id" BIGINT REFERENCES "client_specialty" ("id") ON DELETE NO ACTION
);
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "clients";
        DROP TABLE IF EXISTS "client_groups";
        DROP TABLE IF EXISTS "client_income";
        DROP TABLE IF EXISTS "client_role";
        DROP TABLE IF EXISTS "client_specialty";"""
