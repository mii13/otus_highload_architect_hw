from datetime import datetime
import json
from typing import List
import aioredis
from config import settings
from src.apps.post.containers import Post, serialize_post, deserialize_posts
from src.apps.post.repository import PostRepository


class NewsFeedRepository:
    redis = aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        encoding='utf-8',
        decode_responses=True,
    )

    async def get_posts(self, user_id) -> List[Post]:
        async with self.redis.client() as conn:
            posts = await conn.get(f'{user_id}')
        if posts is None:
            return []
        return deserialize_posts(posts)

    async def add_post(self, user_id: int, post: Post):
        async with self.redis.client() as conn:
            posts = await conn.get(f'{user_id}')
            if posts is None:
                posts = []
            else:
                posts = deserialize_posts(posts)
            posts.append(post)
            posts.sort(key=lambda x: x.created_at, reverse=True)
            # fixMe: may be race condition: use optimistic lock
            await conn.set(f'{user_id}', serialize_post(posts))

        return post

    async def refresh(self, user_id):
        posts = await PostRepository().get_posts(user_id)
        async with self.redis.client() as conn:
            await conn.set(f'{user_id}', serialize_post(posts))
