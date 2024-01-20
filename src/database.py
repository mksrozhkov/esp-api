# stdlib
from typing import AsyncIterator

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# project
from src.config import settings

engine = create_async_engine(settings.DB_URL)  # to debug: echo=True

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
