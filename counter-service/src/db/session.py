from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings

engine = create_async_engine(
    settings.database_url,
    future=True,
    echo=settings.debug,
    pool_size=20,
    # connect_args={"options": "-c timezone=utc"},
)

async_session = sessionmaker(bind=engine, class_=AsyncSession)
