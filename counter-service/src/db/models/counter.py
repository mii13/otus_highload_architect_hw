from sqlalchemy import (
    Column,
    Integer,
)
from src.db.models.base import Base
from src.db.models.mixins import TimestampMixin
from sqlalchemy import UniqueConstraint


class Counter(TimestampMixin, Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint('user_id', 'chat_id', name='uix_1'),
    )
