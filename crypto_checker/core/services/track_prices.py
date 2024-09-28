from decimal import Decimal

from crypto_checker.core.models.dto import User, CryptoPair
from crypto_checker.infrastructure.binance import BinanceClient
from crypto_checker.infrastructure.db.repositories import CryptoPairRepository, UserRepository
from ..exceptions import PairNotFound, PairExists, PairsLimitExceeded


async def add_pair(
    pair_name: str,
    user: User,
    repository: CryptoPairRepository,
    binance_client: BinanceClient,
) -> CryptoPair:
    if len(user.pairs) >= 50:
        raise PairsLimitExceeded

    found_pairs = await binance_client.get_pairs_price([pair_name])
    if current_price := found_pairs.get(pair_name):
        if pair_name in {p.name for p in user.pairs}:
            raise PairExists(f"{pair_name} is already being tracked")

        pair = await repository.add(CryptoPair(name=pair_name, price=Decimal(current_price), user_id=user.id))
        await repository.commit()
        user.pairs.append(pair)
        return pair

    raise PairNotFound


async def remove_pair(
    pair_name: str,
    user: User,
    repository: CryptoPairRepository,
) -> str:
    if not await repository.remove(pair_name, user.id):
        raise PairNotFound

    user.remove_pair(pair_name)
    await repository.commit()
    return pair_name


async def change_percent(user: User, new_percent: Decimal, repository: UserRepository):
    await repository.update_percent(user.id, new_percent)
    user.percent = new_percent
    await repository.commit()
