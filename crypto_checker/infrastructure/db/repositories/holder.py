from sqlalchemy.ext.asyncio import AsyncSession

from .pair import CryptoPairRepository
from .user import UserRepository


class Repository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._user = UserRepository(session)
        self._pair = CryptoPairRepository(session)

    async def commit(self):
        await self._session.commit()

    @property
    def user(self) -> UserRepository:
        return self._user

    @property
    def pair(self) -> CryptoPairRepository:
        return self._pair
