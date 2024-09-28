from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError

from crypto_checker.core.exceptions import PairExists
from crypto_checker.core.models import dto
from .base import BaseRepository
from ..models import CryptoPair


class CryptoPairRepository(BaseRepository):
    async def add(self, pair_dto: dto.CryptoPair) -> dto.CryptoPair:
        pair = CryptoPair.from_dto(pair_dto)

        self._save(pair)
        try:
            await self._flush(pair)
        except IntegrityError:
            raise PairExists

        return pair.to_dto()

    async def remove(self, pair_name: str, user_id: int) -> str | None:
        result = await self._session.execute(
            delete(CryptoPair)
            .where(CryptoPair.name == pair_name, CryptoPair.user_id == user_id)
            .returning(CryptoPair.name)
        )
        return result.scalar()

    async def upsert(self, pairs: list[dto.CryptoPair]):
        query = pg_insert(CryptoPair).values(
            [{"name": pair.name, "user_id": pair.user_id, "price": pair.price} for pair in pairs]
        )
        await self._session.execute(
            query.on_conflict_do_update(
                index_elements=[CryptoPair.name, CryptoPair.user_id],
                set_={"price": query.excluded.price},
            )
        )
