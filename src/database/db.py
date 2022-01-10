import os
from typing import Text

import aiomysql

db_host = os.environ['DB_HOST']
db_port = int(os.environ['DB_PORT'])
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']


async def get_connection(loop):
    conn = await aiomysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        db=db_name,
        loop=loop,
        autocommit=True,
    )
    return conn


async def run_sql(connection, sql: Text, args=None):
    async with connection as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, args)
            return await cursor.fetchall()
