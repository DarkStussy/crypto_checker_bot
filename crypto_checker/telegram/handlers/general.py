from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..keyboards.inline import INLINE_MENU_KB
from ..utils import delete_message


async def menu_command(message: Message, state: FSMContext):
    await message.answer("Menu:", reply_markup=INLINE_MENU_KB)
    await state.clear()


async def back_to_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Menu:", reply_markup=INLINE_MENU_KB)
    await state.clear()


async def callback_hide(callback: CallbackQuery):
    await callback.answer(
        "Не удалось выполнить данное действие" if not await delete_message(callback.message) else None
    )


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(menu_command, Command("start", "menu"))
    router.callback_query.register(back_to_menu, F.data == "back_to_menu")
    router.callback_query.register(callback_hide, F.data == "hide")
    return router
