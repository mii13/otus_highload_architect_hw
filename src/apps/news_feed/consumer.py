import asyncio

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
from config import settings
from src.apps.news_feed.service import NewsFeedService
from src.apps.post.containers import deserialize_post
from src.apps.post.service import PostService
from src.apps.friendship.service import FriendshipService

POST_EXCHANGE_NAME = 'posts'


async def on_create_post(message: AbstractIncomingMessage) -> None:
    async with message.process():
        post_id = int(message.body)
        post = await PostService().get_by_id(post_id)
        if post is None:
            return

        friends = await FriendshipService().get_friends(post.user_id)
        news_feed_service = NewsFeedService()
        for user in friends:
            await news_feed_service.add_post(user.id, post)


async def main() -> None:
    connection = await connect(settings.amqp_url)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        direct_logs_exchange = await channel.declare_exchange(
            name=POST_EXCHANGE_NAME,
            type=ExchangeType.DIRECT,
        )

        queue = await channel.declare_queue(durable=True)

        await queue.bind(direct_logs_exchange, routing_key='all')

        await queue.consume(on_create_post)

        await asyncio.Future()


def start_consume():
    asyncio.run(main())


if __name__ == '__main__':
    start_consume()
