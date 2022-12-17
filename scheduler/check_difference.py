import asyncio
import logging

from aiogram import Bot, types

from database.api.gateways import Gateway
from database.models.user import User
from utils.functions import get_price_of_pairs


async def check_difference_of_pairs(bot: Bot, user: User, gateway: Gateway):
    if user.crypto_pairs:
        prices = await get_price_of_pairs(user.crypto_pairs)
        for pair, price_now in zip(user.crypto_pairs.items(), prices):
            try:
                price_now = float(price_now)
            except Exception as e:
                logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
            else:
                currency = pair[0]
                price = pair[1]
                price_now = float(price_now)
                if abs(100.0 - (price * 100 / price_now)) > user.percent:
                    user.crypto_pairs[currency] = price_now
                    await gateway.merge(user)
                    await bot.send_message(chat_id=user.id, text=f'<b>WARNING:</b>\n'
                                                                 f'{currency} REQUEST: <i>{price:g}</i>\n'
                                                                 f'{currency} NOW: <i>{price_now:g}</i>\n'
                                                                 f'Difference: <i>{price_now - price:g}, '
                                                                 f'{round(100.0 - (price * 100 / price_now), 3)}%</i>',
                                           parse_mode=types.ParseMode.HTML)

    return


async def check_user_pair(bot: Bot, db_session):
    gateway = Gateway(db_session)
    users = await gateway.user.get_all_users()
    for user in users:
        asyncio.create_task(check_difference_of_pairs(bot, user, gateway))
