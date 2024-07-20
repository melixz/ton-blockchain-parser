import json
import asyncio
from db import get_db_pool


async def export_to_json():
    db_pool = await get_db_pool()
    async with db_pool.acquire() as conn:
        addresses = await conn.fetch("SELECT * FROM addresses")
        data = [dict(record) for record in addresses]
        with open('addresses.json', 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    asyncio.run(export_to_json())
