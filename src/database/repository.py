import asyncio
from .db import get_connection, run_sql


class BaseRepository:
    async def run_sql(self, query, args):
        return await run_sql(
            await get_connection(asyncio.get_running_loop()),
            query, args,
        )
