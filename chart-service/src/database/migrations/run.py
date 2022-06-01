import os
import aiomysql

import asyncio
from ..connection import do_query, get_connection

loop = asyncio.get_event_loop()


async def init():
    directory = os.path.dirname(os.path.realpath(__file__))
    files = []
    for file_name in os.listdir(directory):
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            file_name,
        )
        if os.path.isfile(path) and os.path.splitext(file_name)[-1] == '.sql':
            files.append(path)
    files = sorted(files)
    for path in files:
        with open(path, 'r') as f:
            sql = f.read()
        connection = await get_connection(loop)
        try:
            await do_query(connection, sql)
        except Exception as er:
            print(er)
