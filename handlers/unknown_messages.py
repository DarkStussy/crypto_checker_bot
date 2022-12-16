from aiogram import types, Dispatcher
from aiogram.types import ContentType, ChatType


async def unknown_message(message: types.Message):
    await message.reply('My features are slightly limited so I can\'t reply to everything.')


def register_unknown_message(dp: Dispatcher):
    dp.register_message_handler(unknown_message, content_types=ContentType.ANY, chat_type=ChatType.PRIVATE)
