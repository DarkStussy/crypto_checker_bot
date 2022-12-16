import typing
from typing import Any

import aiohttp


async def get_price_of_pairs(pairs: list[str]) -> list[typing.Union[str, None]]:
    prices = []
    async with aiohttp.ClientSession() as session:
        for pair in pairs:
            currency_url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
            async with session.get(currency_url) as resp:
                currency_price = await resp.json()
                prices.append(currency_price.get('price', None))
    return prices


async def get_all_pairs() -> tuple[Any, ...]:
    async with aiohttp.ClientSession() as session:
        currency_url = 'https://api.binance.com/api/v3/exchangeInfo'
        async with session.get(currency_url) as resp:
            pairs = await resp.json()
            return tuple(pair['symbol'] for pair in pairs['symbols'])
