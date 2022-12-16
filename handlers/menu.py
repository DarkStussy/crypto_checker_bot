from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatType

from keyboard.inline import inline_kb_menu


async def send_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Menu:', reply_markup=inline_kb_menu)


async def close(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.finish()


def register_menu(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(send_menu, commands=['start', 'menu'], state='*', chat_type=ChatType.PRIVATE)

    # callback handlers
    dp.register_callback_query_handler(close, Text('close'), state='*')
