from typing import Text
from itertools import cycle

import aiomysql

from config import settings


async def get_connection(loop):
    conn = await aiomysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
        loop=loop,
        autocommit=True,
    )
    return conn


if settings.db_replicas:
    _next_connection = cycle(settings.db_replicas)

    async def get_replica_connection(loop):
        connection = next(_next_connection)
        conn = await aiomysql.connect(
            host=connection.host,
            port=connection.port,
            user=settings.db_user,
            password=settings.db_password,
            db=settings.db_name,
            loop=loop,
            autocommit=True,
        )
        return conn
else:
    get_replica_connection = get_connection


async def run_sql(connection, sql: Text, args=None):
    async with connection as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, args)
            return await cursor.fetchall()
