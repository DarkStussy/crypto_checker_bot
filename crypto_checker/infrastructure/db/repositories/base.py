from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self):
        await self._session.commit()

    def _save(self, obj: Base):
        self._session.add(obj)

    async def _flush(self, *objects: Base):
        await self._session.flush(objects)
