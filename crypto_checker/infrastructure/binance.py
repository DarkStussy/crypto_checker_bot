import json
from decimal import Decimal

from aiohttp import ClientSession


class BinanceClient:
    def __init__(self, session: ClientSession):
        self._session = session
        self._base_url = "https://api.binance.com/api/v3"

    async def get_pairs_price(self, pairs: list[str]) -> dict[str, Decimal]:
        url = f'{self._base_url}/ticker/price?symbols={json.dumps(pairs, separators=(",", ":"))}'
        async with self._session.get(url) as resp:
            return {pair["symbol"]: Decimal(pair["price"]).normalize() for pair in await resp.json()}

    async def get_all_pairs(self) -> dict[str, Decimal]:
        async with self._session.get(f"{self._base_url}/ticker/price") as resp:
            return {pair["symbol"]: Decimal(pair["price"]).normalize() for pair in await resp.json()}
