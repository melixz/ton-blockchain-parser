import asyncio
from pytoniq import LiteClient
from block_scanner import BlockScanner
from db import init_db, get_db_pool
from worker import address_worker
from handle_block import handle_block


async def run_main():
    await init_db()
    db_pool = await get_db_pool()

    while True:
        client = LiteClient.from_mainnet_config(ls_i=14, trust_level=0, timeout=20)
        try:
            await client.connect()
            scanner = BlockScanner(
                client=client,
                block_handler=lambda block: handle_block(block, client, db_pool),
            )
            await asyncio.gather(scanner.run(), address_worker(db_pool))
        except Exception as e:
            print(f"Error: {e}")
            await client.close()
            await asyncio.sleep(10)
        finally:
            await client.close()


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_main())
    except Exception as e:
        print(f"Unhandled exception: {e}")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
