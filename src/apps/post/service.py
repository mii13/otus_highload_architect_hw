from typing import List
from config import settings
from src.apps.post.repository import PostRepository
from src.apps.post.containers import Post
from src.apps.news_feed.repository import NewsFeedRepository
from aio_pika import DeliveryMode, Message, connect, ExchangeType


async def publish(post: Post):
    body = bytes(f'{post.id}', 'utf-8')
    message = Message(body, delivery_mode=DeliveryMode.NOT_PERSISTENT)
    connection = await connect(settings.amqp_url)
    async with connection:
        channel = await connection.channel()
        logs_exchange = await channel.declare_exchange(
            "posts", ExchangeType.DIRECT,
        )
        await logs_exchange.publish(message, routing_key='all')


class PostService:
    def __init__(self):
        self.repository = PostRepository()

    async def create_post(self, user_id, text):
        post_id = await self.repository.create_post(user_id, text)
        post = await self.repository.get_by_id(post_id)
        await NewsFeedRepository().add_post(post.user_id, post)
        await publish(post)
        return post

    async def get_post(self, user_id: int, limit: int = 1000) -> List[Post]:
        return await self.repository.get_posts(user_id, limit)

    async def get_by_id(self, post_id: int) -> Post:
        return await self.repository.get_by_id(post_id)
