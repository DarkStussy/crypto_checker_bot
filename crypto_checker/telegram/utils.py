from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup


async def delete_message(message: Message) -> bool:
    try:
        await message.delete()
        return True
    except TelegramBadRequest:
        return False


async def edit_or_send_message_by_id(
    bot: Bot,
    chat_id: int | str,
    message_id: int | str,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> Message | None:
    try:
        return await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            return await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    return None
