import logging

from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    result = await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Start bot"),
            BotCommand(command="menu", description="Show menu"),
            BotCommand(command="check", description="Check price changes since last request"),
            BotCommand(command="get_price", description="Get current price of cryptocurrency pair"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    if not result:
        logger.error("Can't set bot commands")
