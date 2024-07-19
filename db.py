import asyncpg
from config import DB_DSN


async def init_db():
    async with asyncpg.create_pool(dsn=DB_DSN) as pool:
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    address TEXT PRIMARY KEY,
                    status INTEGER,
                    code TEXT,
                    data TEXT,
                    unixtime INTEGER
                )
            """)


async def get_db_pool():
    return await asyncpg.create_pool(dsn=DB_DSN)
