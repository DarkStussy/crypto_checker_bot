from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ChatType
from aiogram.utils.exceptions import MessageCantBeDeleted

from keyboard.inline import inline_kb_menu


async def send_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Menu:', reply_markup=inline_kb_menu)


async def close(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await callback_query.message.delete()
    except MessageCantBeDeleted:
        pass
    else:
        await state.finish()


async def back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text('Menu:', reply_markup=inline_kb_menu)
    await state.finish()


def register_menu(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(send_menu, commands=['start', 'menu'], state='*', chat_type=ChatType.PRIVATE)

    # callback handlers
    dp.register_callback_query_handler(close, Text('close'), state='*')
    dp.register_callback_query_handler(back_to_menu, Text('back_to_menu'), state='*')
