from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from ..config import Config
from ..infrastructure.binance import BinanceClient
from ..infrastructure.db.provider import DbProvider
from ..telegram.exception_handlers import setup as setup_exceptions_handlers
from ..telegram.handlers import general_router, check_prices_router, track_prices_router
from ..telegram.middlewares import InfrastructureMiddleware, UserMiddleware


async def _setup_outer_middlewares(dispatcher: Dispatcher, db_provider: DbProvider, binance_client: BinanceClient):
    dispatcher.update.outer_middleware(InfrastructureMiddleware(db_provider, binance_client))
    dispatcher.update.outer_middleware(UserMiddleware())


async def create_dispatcher(config: Config, db_provider: DbProvider, binance_client: BinanceClient) -> Dispatcher:
    dispatcher = Dispatcher(name="main_dispatcher", storage=MemoryStorage(), config=config.bot)
    dispatcher.include_routers(general_router(), check_prices_router(), track_prices_router())
    await _setup_outer_middlewares(dispatcher, db_provider, binance_client)
    setup_exceptions_handlers(dispatcher)
    return dispatcher
