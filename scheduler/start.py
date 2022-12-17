import asyncio

import aioschedule
from aiogram import Bot

from scheduler.check_difference import check_user_pair


async def scheduler(bot: Bot, db_session):
    aioschedule.every(5).seconds.do(check_user_pair, bot=bot, db_session=db_session)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)
