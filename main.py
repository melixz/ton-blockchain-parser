import asyncio
from pytoniq import LiteClient
from block_scanner import BlockScanner
from db import init_db, get_db_pool
from worker import address_worker
from handle_block import handle_block


async def main():
    await init_db()
    db_pool = await get_db_pool()
    client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2, timeout=15)
    await client.connect()

    scanner = BlockScanner(client=client, block_handler=lambda block: handle_block(block, client, db_pool))
    await asyncio.gather(scanner.run(), address_worker(db_pool))


if __name__ == "__main__":
    asyncio.run(main())
