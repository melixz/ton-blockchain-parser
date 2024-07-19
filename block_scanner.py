import asyncio
from pytoniq_core import BlockIdExt


class BlockScanner:
    def __init__(self, client, block_handler):
        self.client = client
        self.block_handler = block_handler

    async def run(self):
        while True:
            block = await self.get_latest_block()
            await self.block_handler(block)
            await asyncio.sleep(10)

    async def get_latest_block(self):
        pass
