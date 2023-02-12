import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BadRequest
from aiohttp import ClientSession

from keyboard.inline import inline_kb_back_to_menu, inline_kb_close
from states.check_price import CheckPrice
from utils.functions import get_price_of_pairs


async def get_price_callback(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter cryptocurrency pair.\n'
                                           f'Use <code>@{bot.username}'
                                           f'</code> to view all pairs',
                                           reply_markup=inline_kb_back_to_menu,
                                           parse_mode=types.ParseMode.HTML)
    await CheckPrice.cryptocurrency.set()


async def get_price_command(message: types.Message):
    bot = await message.bot.get_me()
    await message.answer(f'Enter cryptocurrency pair.\n'
                         f'Use <code>@{bot.username}</code> to view all pairs',
                         reply_markup=inline_kb_back_to_menu,
                         parse_mode=types.ParseMode.HTML)
    await CheckPrice.cryptocurrency.set()


async def enter_pair(message: types.Message, client_session: ClientSession,
                     state: FSMContext):
    pair_name = str(message.text.upper())
    pair = await get_price_of_pairs(client_session, [pair_name])
    price = pair.get(pair_name)
    try:
        await message.answer(
            f'<b>{pair_name} price:</b> <i>{float(price):g}</i>',
            reply_markup=inline_kb_close,
            parse_mode=types.ParseMode.HTML)
    except (ValueError, TypeError, BadRequest) as e:
        logging.error(
            f'Error: {type(e).__name__}, file: {__file__}, '
            f'line: {e.__traceback__.tb_lineno}')
        await message.answer(
            'There were some problems, please try again later.')
    finally:
        await state.finish()


def register_get_price(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(enter_pair, state=CheckPrice.cryptocurrency,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(get_price_command, commands=['getprice'])

    # callback handlers
    dp.register_callback_query_handler(get_price_callback, Text('get_price'))
