from pytoniq_core import BlockIdExt


async def handle_block(block: BlockIdExt, client, db_pool):
    if block.workchain == -1:
        return

    transactions = await client.raw_get_block_transactions_ext(block)
    async with db_pool.acquire() as conn:
        for transaction in transactions:
            address = transaction.in_msg.dest
            if address:
                await conn.execute(
                    "INSERT INTO addresses (address, status) VALUES ($1, $2) ON CONFLICT (address) DO NOTHING",
                    address, 0
                )
