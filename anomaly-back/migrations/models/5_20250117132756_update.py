from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clients" ADD "status" VARCHAR(9) NOT NULL  DEFAULT 'new';
        ALTER TABLE "events" ADD "status" VARCHAR(9) NOT NULL  DEFAULT 'wait';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clients" DROP COLUMN "status";
        ALTER TABLE "events" DROP COLUMN "status";"""
