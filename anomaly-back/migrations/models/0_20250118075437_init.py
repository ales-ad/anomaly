from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cities" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(31),
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
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
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "phone" VARCHAR(31),
    "role" VARCHAR(31),
    "login" VARCHAR(127)  UNIQUE,
    "password" VARCHAR(127),
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "events" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(31),
    "date" DATE,
    "status" VARCHAR(9) NOT NULL  DEFAULT 'wait',
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "city_id" BIGINT NOT NULL REFERENCES "cities" ("id") ON DELETE NO ACTION,
    "moderator_id" BIGINT REFERENCES "users" ("id") ON DELETE NO ACTION
);
COMMENT ON COLUMN "events"."status" IS 'wait: wait\nstart: start\ngenerated: generated';
CREATE TABLE IF NOT EXISTS "client_groups" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "number" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event_id" BIGINT NOT NULL REFERENCES "events" ("id") ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS "clients" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tg_username" VARCHAR(100),
    "tg_id" VARCHAR(100),
    "name" VARCHAR(100),
    "age" INT,
    "link"  VARCHAR(200),
    "status" VARCHAR(9) NOT NULL  DEFAULT 'new',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event_id" BIGINT NOT NULL REFERENCES "events" ("id") ON DELETE NO ACTION,
    "groups_id" BIGINT REFERENCES "client_groups" ("id") ON DELETE NO ACTION,
    "income_id" BIGINT REFERENCES "client_income" ("id") ON DELETE NO ACTION,
    "role_id" BIGINT REFERENCES "client_role" ("id") ON DELETE NO ACTION,
    "specialty_id" BIGINT REFERENCES "client_specialty" ("id") ON DELETE NO ACTION
);
COMMENT ON COLUMN "clients"."status" IS 'new: new\ncompleted: completed';
CREATE TABLE IF NOT EXISTS "user_sessions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "refresh_token" VARCHAR(255),
    "last_refresh" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
