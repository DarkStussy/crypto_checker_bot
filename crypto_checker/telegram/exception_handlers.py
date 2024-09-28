import logging

from aiogram import Dispatcher, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message, CallbackQuery

from crypto_checker.core.exceptions import CryptoCheckerError

logger = logging.getLogger(__name__)


async def handle_bot_exception_from_message(event: ErrorEvent, message: Message):
    logger.warning(f"{message.from_user.id}: error: {event.exception.__class__.__name__}")
    await message.reply(getattr(event.exception, "message"))


async def handle_bot_exception_from_callback(event: ErrorEvent, callback: CallbackQuery):
    logger.warning(f"{callback.from_user.id}: error: {event.exception.__class__.__name__}")
    await callback.answer(getattr(event.exception, "message"), show_alert=True)


async def handle_unhandled_exceptions(event: ErrorEvent):
    chat_id = None
    update = event.update
    if update.event_type == "message":
        chat_id = update.message.chat.id
    elif update.event_type == "callback_query":
        chat_id = update.callback_query.message.chat.id

    logger.exception(event.exception, extra={"chat_id": chat_id})
    if chat_id:
        await event.update.bot.send_message(chat_id=chat_id, text="Произошла неизвестная ошибка")


def setup(dispatcher: Dispatcher):
    dispatcher.errors.register(
        handle_bot_exception_from_message,
        ExceptionTypeFilter(CryptoCheckerError),
        F.update.message.as_("message"),
    )
    dispatcher.errors.register(
        handle_bot_exception_from_callback,
        ExceptionTypeFilter(CryptoCheckerError),
        F.update.callback_query.as_("callback"),
    )
    dispatcher.errors.register(handle_unhandled_exceptions)
