from typing import NamedTuple, Optional
from src.database.repository import BaseRepository


class User(NamedTuple):
    id: int
    email: str
    name: str
    second_name: str
    age: int
    gender: str
    interests: str
    city: str
    password: str


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
            return User(*res[0])
        return None
