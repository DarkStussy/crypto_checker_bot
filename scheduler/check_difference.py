import asyncio
import logging

from aiogram import Bot, types
from aiohttp import ClientSession

from database.api.gateways import Gateway
from database.models.user import User
from utils.functions import get_price_of_pairs


async def check_difference_of_pairs(bot: Bot, user: User, gateway: Gateway, client_session: ClientSession):
    if not user.crypto_pairs:
        return

    pairs = await get_price_of_pairs(client_session, user.crypto_pairs)
    if not pairs:
        return

    for pair in user.crypto_pairs.items():
        currency_name = pair[0]
        price = float(pair[1])
        price_now = pairs.get(currency_name)
        if price_now:
            price_now = float(price_now)
            if abs(100.0 - (price * 100 / price_now)) > user.percent:
                user.crypto_pairs[currency_name] = price_now
                await gateway.merge(user)
                await bot.send_message(chat_id=user.id, text=f'<b>WARNING:</b>\n'
                                                             f'{currency_name} REQUEST: <i>{price:g}</i>\n'
                                                             f'{currency_name} NOW: <i>{price_now:g}</i>\n'
                                                             f'Difference: <i>{price_now - price:g}, '
                                                             f'{round(100.0 - (price * 100 / price_now), 3)}%</i>',
                                       parse_mode=types.ParseMode.HTML)


async def check_user_pair(bot: Bot, db_session, client_session: ClientSession):
    gateway = Gateway(db_session)
    users = await gateway.user.get_all_users()
    for user in users:
        asyncio.create_task(check_difference_of_pairs(bot, user, gateway, client_session))
