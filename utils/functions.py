import json

from aiohttp import ClientSession


async def get_price_of_pairs(session: ClientSession, pairs: list[str]) -> dict:
    url = f'https://api.binance.com/api/v3/ticker/price?' \
          f'symbols={json.dumps(pairs, separators=(",", ":"))}'
    async with session.get(url) as resp:
        result_json = await resp.json()

    return {pair['symbol']: pair['price'] for pair in result_json}


async def get_all_pairs(session: ClientSession) -> list[str]:
    url = 'https://api.binance.com/api/v3/ticker/price'
    async with session.get(url) as resp:
        pairs = await resp.json()
        return [pair['symbol'] for pair in pairs]
