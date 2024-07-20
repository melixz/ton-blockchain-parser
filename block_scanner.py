import asyncio
from pytoniq_core import BlockIdExt


class BlockScanner:
    def __init__(self, client, block_handler):
        self.client = client
        self.block_handler = block_handler

    async def run(self):
        while True:
            block = await self.get_latest_block()
            if block:
                await self.block_handler(block)
            await asyncio.sleep(10)

    async def get_latest_block(self):
        try:
            last_block = await self.client.get_masterchain_info()
            last_block_id = BlockIdExt(
                workchain=-1,
                shard=-9223372036854775808,
                seqno=last_block.last.seqno
            )
            return last_block_id
        except Exception as e:
            print(f"Error getting latest block: {e}")
            return None
