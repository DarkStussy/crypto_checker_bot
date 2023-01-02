import asyncio
from typing import Any

from aiohttp import ClientSession


class BinanceAPIError(Exception):
    def __init__(self, code: int, message: str = 'Unknown request error'):
        self.message = message
        self.code = code
        super().__init__(self.message)


async def get_price_task(session: ClientSession, currency_url: str) -> dict:
    async with session.get(currency_url) as resp:
        data = await resp.json()
        status_code = data.get('code')
        if status_code is None:
            return data

        if status_code == -1003:
            raise BinanceAPIError(status_code, 'Too many requests')
        elif status_code == -1121:
            raise BinanceAPIError(status_code, 'Invalid symbol')
        else:
            raise BinanceAPIError(status_code)


async def get_price_of_pairs(session: ClientSession, pairs: list[str]) -> dict:
    pending_tasks = []
    pairs_result = {}
    for pair in pairs:
        currency_url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
        pending_tasks.append(asyncio.create_task(get_price_task(session, currency_url)))
    while pending_tasks:
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks,
                                                       return_when=asyncio.FIRST_COMPLETED)
        for done_task in done_tasks:
            exception = done_task.exception()
            if exception is None:
                task_result = done_task.result()
                pairs_result[task_result['symbol']] = task_result['price']
            elif exception.code == -1003:
                [task.cancel() for task in pending_tasks]
                return pairs_result

    return pairs_result


async def get_all_pairs(session: ClientSession) -> tuple[Any]:
    currency_url = 'https://api.binance.com/api/v3/exchangeInfo'
    async with session.get(currency_url) as resp:
        pairs = await resp.json()
        return tuple(pair.get('symbol') for pair in pairs['symbols'] if pair.get('symbol') is not None)
