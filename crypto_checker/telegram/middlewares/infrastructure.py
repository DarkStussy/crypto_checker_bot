from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ...infrastructure.binance import BinanceClient
from ...infrastructure.db.provider import DbProvider


class InfrastructureMiddleware(BaseMiddleware):
    def __init__(self, db_provider: DbProvider, binance_client: BinanceClient) -> None:
        self._db_provider = db_provider
        self._binance_client = binance_client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self._db_provider() as repository:
            data.update({"repository": repository, "binance_client": self._binance_client})
            return await handler(event, data)
