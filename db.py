import asyncpg
from config import DB_DSN


async def init_db():
    pool = await asyncpg.create_pool(dsn=DB_DSN)
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses (
                address TEXT PRIMARY KEY,
                status INTEGER,
                code TEXT,
                data TEXT,
                unixtime INTEGER
            )
        """
        )
    return pool


async def get_db_pool():
    return await asyncpg.create_pool(dsn=DB_DSN)
