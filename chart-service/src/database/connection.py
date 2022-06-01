from typing import List, NamedTuple, Text

import aiomysql
import crcmod

from src.settings import settings

crc16 = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)


class ConnectionConfig(NamedTuple):
    host: str
    port: int
    db: str
    user: str
    password: str

    def as_dict(self):
        return self._asdict()


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


shards: List[ConnectionConfig] = [
    ConnectionConfig(
        host=shard.host, port=shard.port,
        db=settings.db_name,
        user=settings.db_user,
        password=settings.db_password
    )
    for shard in settings.db_shards
]


def get_shard_key(chat_id: int) -> int:
    return crc16(bytes(f'{chat_id}', 'utf-8'))


async def get_shard_connection(chat_id: int, loop):
    key = get_shard_key(chat_id)
    config = shards[key % len(shards)]
    return await aiomysql.connect(
        **config.as_dict(),
        loop=loop,
        autocommit=True,
    )


async def do_query(connection, sql: Text, args=None):
    async with connection as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, args)
            return await cursor.fetchall()


async def insert(connection, sql: Text, args=None):
    async with connection as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, args)
            return cursor.lastrowid
