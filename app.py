import asyncio
import logging

import aiohttp
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.orm import sessionmaker

from config import load_config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from database.base import Base
from aiogram import Dispatcher, Bot

from filters.admin import AdminFilter
from handlers import setup_handlers
from middlewares.client_session import ClientSessionMiddleware
from middlewares.database import DatabaseMiddleware
from middlewares.role import RoleMiddleware
from middlewares.throttling import ThrottlingMiddleware

from utils.set_bot_commands import set_default_commands
from utils.notify_admins import notify_admins

from scheduler.start import scheduler


async def create_engine(host: str, password: str, username: str, database: str) -> AsyncEngine:
    engine = create_async_engine(
        f'postgresql+asyncpg://{username}:{password}@{host}/'
        f'{database}', echo=False, future=True)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return engine


async def main():
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s | %(name)s - %(levelname)s - %(message)s')

    config = load_config()
    if config.bot.use_redis:
        storage = RedisStorage2('localhost', 6379, db=5, pool_size=10)
    else:
        storage = MemoryStorage()

    engine = await create_engine(config.db.host, config.db.password, config.db.username, config.db.database)
    db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    client_session = aiohttp.ClientSession()

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(ThrottlingMiddleware(limit=1))
    dp.middleware.setup(RoleMiddleware(config.bot.admins))
    dp.middleware.setup(DatabaseMiddleware(db_session))
    dp.middleware.setup(ClientSessionMiddleware(client_session))

    dp.filters_factory.bind(AdminFilter)

    setup_handlers(dp)

    await set_default_commands(dp)
    await notify_admins(dp, config.bot.admins)

    asyncio.create_task(scheduler(bot, db_session, client_session))

    try:
        logging.warning('Bot started!')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()
        await engine.dispose()
        await client_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")
