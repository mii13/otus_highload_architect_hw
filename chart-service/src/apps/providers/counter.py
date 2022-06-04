from httpx import AsyncClient
from urllib.parse import urljoin


class CounterTransactionError(Exception):
    """"""


class CounterClient:
    def __init__(self, url):
        self.url = url

    async def increment(self, user_id, chat_id, cnt=1):
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = '/counter/inc/'

            url = urljoin(self.url, endpoint)

            response = await client.post(
                url=url,
                json=dict({'chat_id': chat_id, 'user_id': user_id, 'count': cnt}),
            )
            if response.status_code != 201:
                raise CounterTransactionError()

            return response.json()

    async def decrement(self, user_id, chat_id, cnt=1):
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = '/counter/dec/'
            url = urljoin(self.url, endpoint)
            response = await client.post(
                url=url,
                json=dict({'chat_id': chat_id, 'user_id': user_id, 'count': cnt}),
            )
            return response.json()

    async def list(self, user_id):
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = f'/counter/{user_id}/'
            response = await client.get(urljoin(self.url, endpoint))
            return response.json()

