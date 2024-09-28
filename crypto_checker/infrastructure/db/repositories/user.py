from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from crypto_checker.core.exceptions import UserNotFound
from crypto_checker.core.models import dto
from .base import BaseRepository
from ..models import User


class UserRepository(BaseRepository):
    async def get_by_id(self, user_id: int) -> dto.User:
        user = await self._session.scalar(select(User).where(User.id == user_id).options(joinedload(User.pairs)))
        if not user:
            raise UserNotFound

        return user.to_dto()

    async def create(self, user_dto: dto.User) -> dto.User:
        user = User.from_dto(user_dto)
        self._save(user)
        try:
            await self._session.flush([user])
        except IntegrityError:
            pass

        return user.to_dto(with_pairs=False)

    async def get_all(self) -> list[dto.User]:
        result = await self._session.execute(select(User).options(joinedload(User.pairs)))
        return [user.to_dto() for user in result.unique().scalars().all()]

    async def update_percent(self, user_id: int, percent: Decimal):
        await self._session.execute(update(User).where(User.id == user_id).values({"percent": percent}))
