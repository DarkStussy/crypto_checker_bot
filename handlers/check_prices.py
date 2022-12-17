from aiogram import Dispatcher, types

from database.api.gateways import Gateway
from keyboard.inline import inline_kb_close
from utils.functions import get_price_of_pairs


async def check_prices(message: types.Message, gateway: Gateway):
    message_text = ""
    user = await gateway.user.get_by_chat_id(message.chat.id)

    if user.crypto_pairs:
        prices = await get_price_of_pairs(user.crypto_pairs)
        for pair, price_now in zip(user.crypto_pairs.items(), prices):
            currency_pair = pair[0]
            price = pair[1]
            price_now = float(price_now)
            message_text += f'<b>{currency_pair}:</b>\nLast request: {price:g}\nNow: ' \
                            f'{price_now:g}\nDifference: ' \
                            f'{price_now - price:g}, ' \
                            f'{round(100.0 - (price * 100 / price_now), 3)}%\n\n'
        await message.answer(message_text, reply_markup=inline_kb_close, parse_mode=types.ParseMode.HTML)


def register_check_prices(dp: Dispatcher):
    dp.register_message_handler(check_prices, commands=['check'])
