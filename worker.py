import time
import asyncio
from pytoniq import LiteBalancer


async def process_addresses(db_pool):
    async with db_pool.acquire() as conn:
        addresses = await conn.fetch("SELECT address FROM addresses WHERE status = 0")
        client = LiteBalancer.from_mainnet_config(trust_level=1)
        await client.start_up()

        for record in addresses:
            address = record["address"]
            result = await client.run_get_method(
                address=address, method="get_code", stack=[]
            )
            code = result["code"]
            data = result["data"]
            unixtime = int(time.time())
            await conn.execute(
                "UPDATE addresses SET status = 1, code = $1, data = $2, unixtime = $3 WHERE address = $4",
                code,
                data,
                unixtime,
                address,
            )
        await client.close_all()


async def address_worker(db_pool):
    while True:
        await process_addresses(db_pool)
        await asyncio.sleep(60)
