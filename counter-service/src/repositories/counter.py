from typing import Optional
from sqlalchemy import select, update
from src.db.models.counter import Counter
from src.repositories.base import BaseRepository
from src.schemas.counter import CounterSchema


class CounterRepository(BaseRepository[Counter]):
    model_class = Counter

    async def list(
        self,
        user_id: int,
    ) -> list[Counter]:
        stmt = (
            select(Counter)
            .where(Counter.user_id==user_id)
        )
        return list(await self.session.scalars(stmt))

    async def get(
        self,
        user_id: int,
        chat_id: int,
    ) -> Counter:
        stmt = (
            select(self.model_class)
            .where(
                self.model_class.user_id == user_id,
                self.model_class.chat_id == chat_id,
            )
        )
        return await self.session.scalar(stmt)

    async def append(
        self,
        counter: CounterSchema,
    ) -> Counter:
        db_counter = await self.get(counter.user_id, counter.chat_id)
        if db_counter is None:
            db_counter = self.model_class(
                user_id=counter.user_id,
                chat_id=counter.chat_id,
                count=counter.count,
            )
            self.session.add(db_counter)
        else:
            db_counter.count += counter.count
        await self.session.flush()

        # stmt = (
        #     update(self.model_class)
        #     .values(counter=self.model_class.count + counter.count)
        #     .where(chat_id=counter.chat_id, user_id=counter.chat_id)
        # )

        return db_counter

    async def decrement(
        self,
        counter: CounterSchema,
    ) -> Optional[Counter]:
        stmt = (
            update(self.model_class)
            .values(count=(self.model_class.count - counter.count))
            .where(
                self.model_class.chat_id == counter.chat_id,
                self.model_class.user_id == counter.user_id,
            )
        )
        await self.session.execute(stmt)

        return await self.get(counter.user_id, counter.chat_id)
