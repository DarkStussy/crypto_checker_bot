import asyncio

import aioschedule
from aiogram import Bot
from aiohttp import ClientSession

from scheduler.check_difference import check_user_pair


async def scheduler(bot: Bot, db_session, client_session: ClientSession):
    aioschedule.every(3).seconds.do(check_user_pair, bot=bot,
                                    db_session=db_session,
                                    client_session=client_session)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
