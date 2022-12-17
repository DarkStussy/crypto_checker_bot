from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboard.inline import inline_kb_back_to_menu, inline_kb_close
from states.check_price import CheckPrice
from utils.functions import get_price_of_pairs


async def get_price(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter cryptocurrency pair.\n'
                                           f'Use <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_back_to_menu, parse_mode=types.ParseMode.HTML)
    await CheckPrice.cryptocurrency.set()


async def enter_pair(message: types.Message, state: FSMContext):
    pair = str(message.text)
    price = (await get_price_of_pairs([pair]))[0]
    if price:
        await state.finish()
        return await message.answer(f'{pair} price: {float(price):g}', reply_markup=inline_kb_close)

    await message.answer('Invalid cryptocurrency pair')


def register_get_price(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(enter_pair, state=CheckPrice.cryptocurrency,
                                content_types=types.ContentTypes.TEXT)

    # callback handlers
    dp.register_callback_query_handler(get_price, Text('get_price'))
