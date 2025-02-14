from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clients" ADD "count_group_current" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "clients" ADD "is_leader" BOOL NOT NULL  DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clients" DROP COLUMN "count_group_current";
        ALTER TABLE "clients" DROP COLUMN "is_leader";"""
