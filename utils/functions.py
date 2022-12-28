import asyncio
import typing
from typing import Any

from aiohttp import ClientSession


async def get_price_task(session: ClientSession, currency_url: str) -> typing.Union[str, None]:
    async with session.get(currency_url) as resp:
        currency_price = await resp.json()
        return currency_price.get('price')


async def get_price_of_pairs(session: ClientSession, pairs: list[str]) -> \
        tuple[BaseException | Any, ...]:
    coroutines = []
    for pair in pairs:
        currency_url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
        coroutines.append(get_price_task(session, currency_url))
    return await asyncio.gather(*coroutines)


async def get_all_pairs(session: ClientSession) -> tuple[Any]:
    currency_url = 'https://api.binance.com/api/v3/exchangeInfo'
    async with session.get(currency_url) as resp:
        pairs = await resp.json()
        return tuple(pair.get('symbol') for pair in pairs['symbols'] if pair.get('symbol') is not None)
