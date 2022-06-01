from typing import Optional, List
from src.database.repository import BaseRepository
from src.apps.user.containers import Profile


class FriendshipRepository(BaseRepository):
    async def make_friend(self, user1_id, user2_id):
        query = """
        insert into friendship(user_id, friend_id) 
        values (%s, %s), (%s, %s)
        """
        args = (user1_id, user2_id, user2_id, user1_id)
        return await self.run_sql(query, args)

    async def get_friends(self, user_id) -> List[Profile]:
        query = """
            select user.id, email, name, second_name, age, gender, interests, city
            from user inner join friendship on friendship.friend_id = user.id
            where friendship.user_id = %s
        """
        rows = await self.run_sql(query, (user_id,))
        return [Profile(*row) for row in rows]

    async def is_friends(self, user1_id, user2_id) -> bool:
        query = """
            select 1
            from friendship 
            where user_id=%s and friend_id=%s
            limit 1
        """
        rows = await self.run_sql(query, (user1_id, user2_id))
        return bool(len(rows))
