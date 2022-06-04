from typing import Generic, TypeVar

from sqlalchemy.sql.expression import delete, select
from src.db.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    model_class = Base

    def __init__(self, session):
        self.session = session

    async def get(self, object_id: int) -> ModelType | None:
        stmt = select(self.model_class).where(self.model_class.id == object_id)
        return await self.session.scalar(stmt)

    async def delete(self, object_id: int):
        stmt = delete(self.model_class).where(self.model_class.id == object_id)
        await self.session.execute(stmt)
