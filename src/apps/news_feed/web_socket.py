import asyncio
from typing import Dict
from starlette.websockets import WebSocket, WebSocketDisconnect
from config import settings

from aio_pika.abc import AbstractIncomingMessage
from aio_pika import connect, Message, ExchangeType, connect_robust 
from src.apps.post.service import PostService
from src.apps.friendship.service import FriendshipService

import logging

logger = logging.getLogger(__name__)

POST_EXCHANGE_NAME = 'posts'


class WsManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}
        self.rmq_connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

    async def setup(self):
        logger.error('start setup ws consume')
        self.rmq_connection = await connect_robust(settings.amqp_url, loop=asyncio.get_running_loop())
        self.channel = await self.rmq_connection.channel()
        self.exchange = await self.channel.declare_exchange(
            name=POST_EXCHANGE_NAME,
            type=ExchangeType.DIRECT,
        )
        self.queue = await self.channel.declare_queue()
        await self.queue.bind(self.exchange, routing_key='all')
        await self.queue.consume(self.on_message)
        logger.info('end setup ws consume')

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.connections[int(user_id)] = websocket
        logger.info('new websocket connect')

    def remove(self, user_id: int):
        del self.connections[user_id]

    async def on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            post_id = int(message.body)

            post = await PostService().get_by_id(post_id)

            if post is None:
                return

            friends = await FriendshipService().get_friends(post.user_id)
            dead_connections = []
            for user in friends:

                con = self.connections.get(int(user.id))

                if con is None:
                    continue
                try:
                    await con.send_text(
                        f"{post.text} ({post.user_name} {post.user_second_name}, {post.created_at})",
                    )
                except WebSocketDisconnect:
                    logger.info(f'user_id {user.id} ws disconnected')
                    dead_connections.append(user.id)

            for user_id in dead_connections:
                self.remove(user_id)