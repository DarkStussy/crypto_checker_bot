import asyncio
import logging

from aiogram.client.session.aiohttp import AiohttpSession

from crypto_checker.config import load_config
from crypto_checker.factory import create_dispatcher, create_bot
from crypto_checker.infrastructure.binance import BinanceClient
from crypto_checker.infrastructure.db.provider import DbProvider
from crypto_checker.scheduler import run_scheduler
from crypto_checker.utils.commands import set_commands
from crypto_checker.utils.notify import notify_admins

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s - %(levelname)s - %(message)s")
logging.getLogger("aiogram").setLevel(logging.WARNING)


async def main():
    config = load_config()
    session = AiohttpSession()
    bot = create_bot(config.bot, session)
    binance_client = BinanceClient(await session.create_session())
    db_provider = DbProvider(config.db)
    dispatcher = await create_dispatcher(config, db_provider, binance_client)

    try:
        await set_commands(bot)
        await notify_admins(bot, config.bot.admins)
        run_scheduler(bot, db_provider, binance_client, config.scheduler)

        logging.info("Bot started")
        await dispatcher.start_polling(bot)
    finally:
        await db_provider.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
