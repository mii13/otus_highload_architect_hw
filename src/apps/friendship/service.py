from src.apps.friendship.repository import FriendshipRepository
from src.apps.news_feed.service import NewsFeedService


class FriendshipService:
    def __init__(self):
        self.repository = FriendshipRepository()

    async def make_friends(self, user1_id: int, user2_id: int):
        if await self.repository.is_friends(user1_id, user2_id):
            return
        if user1_id == user2_id:
            return
        await self.repository.make_friend(user1_id, user2_id)
        # update news in wall
        news_feed_service = NewsFeedService()
        await news_feed_service.refresh(user1_id)
        await news_feed_service.refresh(user2_id)

    async def get_friends(self, user_id: int):
        return await self.repository.get_friends(user_id)