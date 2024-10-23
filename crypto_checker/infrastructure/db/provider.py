from contextlib import asynccontextmanager
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .repositories import Repository
from ...config import DbConfig


class DbProvider:
    def __init__(self, config: DbConfig):
        self._config = config
        self._engine = create_async_engine(config.url)
        self._pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def __call__(self) -> AsyncIterable[Repository]:
        async with self._pool() as session:
            yield Repository(session)

    async def close(self):
        await self._engine.dispose()
