import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboard.inline import inline_kb_back_to_menu, inline_kb_close
from states.check_price import CheckPrice
from utils.functions import get_price_of_pairs


async def get_price_callback(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter cryptocurrency pair.\n'
                                           f'Use <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_back_to_menu, parse_mode=types.ParseMode.HTML)
    await CheckPrice.cryptocurrency.set()


async def get_price_command(message: types.Message):
    bot = await message.bot.get_me()
    await message.answer(f'Enter cryptocurrency pair.\n'
                         f'Use <code>@{bot.username}</code> to view all pairs',
                         reply_markup=inline_kb_back_to_menu, parse_mode=types.ParseMode.HTML)
    await CheckPrice.cryptocurrency.set()


async def enter_pair(message: types.Message, state: FSMContext):
    pair = str(message.text)
    price = (await get_price_of_pairs([pair]))[0]

    try:
        await message.answer(f'<b>{pair} price:</b> <i>{float(price):g}</i>', reply_markup=inline_kb_close,
                             parse_mode=types.ParseMode.HTML)
    except Exception as e:
        logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
        await message.answer('There were some problems, please try again later.')
    finally:
        await state.finish()


def register_get_price(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(enter_pair, state=CheckPrice.cryptocurrency,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(get_price_command, commands=['getprice'])

    # callback handlers
    dp.register_callback_query_handler(get_price_callback, Text('get_price'))
