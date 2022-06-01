from httpx import AsyncClient
from opentelemetry.propagate import inject
import json
from .schema import Chat, ChatOut, MessageOut, Message
from urllib.parse import urljoin


class ChatService:
    def __init__(self, url):
        self.url = url

    async def create_chat(self, chat: Chat):
        headers = {}
        inject(headers)
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = '/chat/'

            url = urljoin(self.url, endpoint)

            response = await client.post(
                url=url,
                json=dict(chat),
                headers=headers
            )

            return response.json()

    async def get_chats(self, user_id: int):
        headers = {}
        inject(headers)
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = '/chat/'

            url = urljoin(self.url, endpoint)

            response = await client.get(
                url=url,
                params={'user_id': user_id},
                headers=headers,
            )

            return response.json()

    async def get_messages(self, chat_id, message_id):
        headers = {}
        inject(headers)
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = f'/message/chat/{chat_id}/'

            url = urljoin(self.url, endpoint)

            response = await client.get(
                url=url,
                params={'message_id': message_id},
                headers=headers,
            )

            return response.json()

    async def create_message(self, message: Message):
        headers = {}
        inject(headers)
        async with AsyncClient() as client:
            client: AsyncClient
            endpoint = '/message/'

            url = urljoin(self.url, endpoint)

            response = await client.post(
                url=url,
                json=dict(message),
                headers=headers,
            )

            return response.json()
