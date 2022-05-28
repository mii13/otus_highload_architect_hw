# import aiotarantool
import asynctnt
from config.settings import settings
from .containers import User, Profile

client = asynctnt.Connection(host=settings.tarantool_host, port=settings.tarantool_port)


async def search_profiles(
    name: str | None = None,
    second_name: str | None = None,
    limit: int = 10,
) -> list[Profile]:
    # client = aiotarantool.connect(settings.tarantool_host, settings.tarantool_port)
    await client.connect()
    if name and second_name:
        res = await client.call('search', (name, second_name, limit))
    elif name:
        res = await client.call('search_by_name', (name, limit))
    elif second_name:
        res = await client.call('search_by_second_name', (second_name, limit))
    else:
        res = await client.select('user', limit=limit)
        # client.close()
        return [Profile(*row[:-2]) for row in res]

    # client.close()
    result = []
    for rows in res:
        # for row in rows:
        #     row = row[:-1]
        #     print(row)
        #     result.append(Profile(*row))
        return [Profile(*row[:-2]) for row in rows]
    return result
