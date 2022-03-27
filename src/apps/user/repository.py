from typing import Optional, List
from src.database.repository import BaseRepository
from .containers import User, Profile


class UserRepository(BaseRepository):
    async def add_user(
        self, name, second_name, age, gender, city,
        interests, email, password,
    ):
        query = """
        insert into user(name, second_name, age, gender, city, interests, email, password) 
        values (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        args = (
            name, second_name, age, gender.value,
            city, interests, email, password,
        )
        return await self.run_sql(query, args)

    async def get_user(self, email) -> Optional[User]:
        query = """
            select id, email, name, second_name, age, gender, interests, city, password
            from user 
            where email = %s
        """
        res = await self.run_sql(query, (email,))
        if res:
            row = res[0]
            return User(*row)
        return None

    async def search_profiles(
            self, name: str,
            second_name: str,
            limit: int,
            offset: int,
    ) -> List[Profile]:
        where = []
        args = []
        if name:
            where.append(' name like %s ')
            args.append(name )
        if second_name:
            where.append(' second_name like %s ')
            args.append(second_name )
        if where:
            where_str = 'where ' + ' and '.join(where)
        else:
            where_str = ''

        query = f"""
            select id, email, name, second_name, age, gender, interests, city
            from user 
            {where_str}
            order by id
            limit %s, %s 
        """
        res = await self.run_sql(query, args + [offset, limit])
        if res:
            return [Profile(*row) for row in res]
        return []
