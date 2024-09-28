import logging
from collections import defaultdict
from decimal import Decimal

from aiogram import Bot

from crypto_checker.core.models import dto
from crypto_checker.infrastructure.binance import BinanceClient
from crypto_checker.infrastructure.db.provider import DbProvider
from crypto_checker.infrastructure.db.repositories import Repository
from crypto_checker.utils.messages import get_prices_changes_message


def _check_price(
    user: dto.User,
    all_pairs: dict[str, Decimal],
    changed_pairs_map: dict[int, list[dto.CryptoPair]],
    old_pairs_map: dict[int, list[dto.CryptoPair]],
):
    for pair in user.pairs:
        current_price = all_pairs.get(pair.name)
        if current_price is not None and abs(Decimal("100.0") - (pair.price * 100 / current_price)) >= user.percent:
            changed_pairs_map[user.id].append(dto.CryptoPair(name=pair.name, price=current_price, user_id=user.id))
            old_pairs_map[user.id].append(pair)
            logging.info(f"{user.id}: {pair.name}: {pair.price.normalize():f} -> {current_price:f}")


async def check_users_pairs(bot: Bot, db_provider: DbProvider, binance_client: BinanceClient):
    all_pairs = await binance_client.get_all_pairs()
    changed_pairs_map, old_pairs_map = defaultdict(list), defaultdict(list)

    async with db_provider() as repository:
        repository: Repository
        for user in await repository.user.get_all():
            if user.pairs:
                _check_price(user, all_pairs, changed_pairs_map, old_pairs_map)

        if changed_pairs_map:
            await repository.pair.upsert([pair for pairs in changed_pairs_map.values() for pair in pairs])
            await repository.commit()

    for user_id, old_pairs in old_pairs_map.items():
        await bot.send_message(
            chat_id=user.id,
            text="⚠️ <b>ALERT</b> ⚠️\n\n" + get_prices_changes_message(old_pairs, all_pairs),
        )
