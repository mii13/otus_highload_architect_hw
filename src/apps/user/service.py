from config import settings
from .repository import UserRepository
from .tarantool_repository import search_profiles


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_by_id(self, user_id: int):
        return self.repository.get_user_by_id(user_id)

    async def search_profiles(self, name, second_name, limit, offset):
        if settings.tarantool_host:
            return await search_profiles(name, second_name, limit)
        return await self.repository.search_profiles(name, second_name, limit, offset)
