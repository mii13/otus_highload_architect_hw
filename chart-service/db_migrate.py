import asyncio
from src.database.migrations import run
from src.database.shard_migrations import run as shard_run


async def migrate():
    await shard_run.init()
    await run.init()


if __name__ == '__main__':
    asyncio.run(migrate())
