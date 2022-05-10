from typing import List, Optional
from src.database.repository import BaseRepository
from .containers import Post


class PostRepository(BaseRepository):
    async def create_post(self, user_id: int, text: str):
        query = """
        insert into post(user_id, text) 
        values (%s, %s)
        """
        args = (user_id, text)
        return await self.insert(query, args)

    async def get_posts(self, user_id: int, limit: int = 1000) -> List[Post]:
        """return post of the user and his friends."""
        query = """
            (
                select post.id, post.user_id, post.text, post.created_at, user.name, user.second_name
                from post inner join friendship on post.user_id = friendship.friend_id
                inner join user on user.id = post.user_id
                where friendship.user_id = %s
            )
            union 
            (
                select post.id, post.user_id, post.text, post.created_at, user.name, user.second_name
                from post 
                inner join user on user.id = post.user_id
                where post.user_id = %s
            )
            order by created_at desc
            limit %s
        """
        args = (user_id, user_id, limit)
        return [
            Post(*row)
            for row in await self.run_sql(query, args)
        ]

    async def get_by_id(self, post_id) -> Optional[Post]:
        query = """
            select post.id, post.user_id, post.text, post.created_at, user.name, user.second_name
            from post inner join user on post.user_id = user.id
            where post.id = %s
        """
        args = (post_id,)
        for row in await self.run_sql(query, args):
            return Post(*row)
        return None
