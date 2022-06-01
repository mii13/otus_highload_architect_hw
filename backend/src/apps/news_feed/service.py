from .repository import NewsFeedRepository
from src.apps.post.containers import Post


class NewsFeedService:
    def __init__(self):
        self.repository = NewsFeedRepository()

    async def get_posts(self, user_id):
        # todo: add pagination
        return await self.repository.get_posts(user_id)

    async def add_post(self, user_id, post: Post):
        return await self.repository.add_post(user_id, post)

    async def refresh(self, user_id):
        return await self.repository.refresh(user_id)
