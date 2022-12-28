import logging

from aiogram import Dispatcher, types
from aiohttp import ClientSession

from database.api.gateways import Gateway
from keyboard.inline import inline_kb_close
from utils.functions import get_price_of_pairs


async def check_prices(message: types.Message, gateway: Gateway, client_session: ClientSession):
    message_text = ''
    user = await gateway.user.get_by_chat_id(message.chat.id)

    if user.crypto_pairs:
        prices = await get_price_of_pairs(client_session, user.crypto_pairs)
        for pair, price_now in zip(user.crypto_pairs.items(), prices):
            currency_pair = pair[0]
            price = pair[1]
            try:
                price_now = float(price_now)
            except Exception as e:
                logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
            else:
                message_text += f'<b>{currency_pair}:</b>\nLast request: <i>{price:g}</i>\nNow: ' \
                                f'<i>{price_now:g}</i>\nDifference: ' \
                                f'<i>{price_now - price:g}, ' \
                                f'{round(100.0 - (price * 100 / price_now), 3)}%</i>\n\n'
        if message_text:
            await message.answer(message_text, reply_markup=inline_kb_close, parse_mode=types.ParseMode.HTML)


def register_check_prices(dp: Dispatcher):
    dp.register_message_handler(check_prices, commands=['check'])
