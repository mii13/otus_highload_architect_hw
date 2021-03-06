import asyncio
from .db import get_connection, get_replica_connection, run_sql, insert


class BaseRepository:
    async def run_sql(self, query, args):
        return await run_sql(
            await get_connection(asyncio.get_running_loop()),
            query, args,
        )

    async def insert(self, query, args):
        return await insert(
            await get_connection(asyncio.get_running_loop()),
            query, args,
        )

    async def run_replica_sql(self, query, args):
        return await run_sql(
            await get_replica_connection(asyncio.get_running_loop()),
            query, args,
        )
