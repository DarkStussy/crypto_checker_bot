from decimal import Decimal

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from crypto_checker.core.models.dto import User
from ..keyboards.inline import INLINE_TRACK_PRICES_KB, INLINE_BACK_TO_TRACK_PRICES_KB
from ..states.pair import TrackPairs
from ..utils import edit_or_send_message_by_id
from ...core.services import track_prices as services
from ...infrastructure.binance import BinanceClient
from ...infrastructure.db.repositories import Repository
from ...utils.messages import get_tracking_bar_message


async def show_track_prices_panel_callback(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text=get_tracking_bar_message(user.percent, user.pairs),
        reply_markup=INLINE_TRACK_PRICES_KB,
    )


async def add_pair_callback(callback: CallbackQuery, state: FSMContext):
    bot = await callback.bot.get_me()
    message = await callback.message.edit_text(
        f"Enter cryptocurrency pair.\nUse <code>@{bot.username}</code> to view all pairs",
        reply_markup=INLINE_BACK_TO_TRACK_PRICES_KB,
    )
    await state.set_state(TrackPairs.add_pair)
    await state.update_data(message_id=message.message_id)


async def add_pair(
    message: Message,
    state: FSMContext,
    user: User,
    repository: Repository,
    binance_client: BinanceClient,
):
    pair = await services.add_pair(message.text.upper(), user, repository.pair, binance_client)
    await message.answer(f"Tracking has been successfully initiated 🎉\n<b>{pair.name}</b>: {pair.price:f}")
    await edit_or_send_message_by_id(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=(await state.get_data())["message_id"],
        text=get_tracking_bar_message(user.percent, user.pairs),
        reply_markup=INLINE_TRACK_PRICES_KB,
    )
    await state.clear()


async def remove_pair_callback(callback: CallbackQuery, state: FSMContext):
    bot = await callback.bot.get_me()
    message = await callback.message.edit_text(
        f"Enter cryptocurrency pair.\nUse <code>@{bot.username}</code> to view all pairs",
        reply_markup=INLINE_BACK_TO_TRACK_PRICES_KB,
    )
    await state.set_state(TrackPairs.remove_pair)
    await state.update_data(message_id=message.message_id)


async def remove_pair(message: Message, state: FSMContext, user: User, repository: Repository):
    pair_name = await services.remove_pair(message.text.upper(), user, repository.pair)
    await message.answer(f"{pair_name} has successfully removed")
    await edit_or_send_message_by_id(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=(await state.get_data())["message_id"],
        text=get_tracking_bar_message(user.percent, user.pairs),
        reply_markup=INLINE_TRACK_PRICES_KB,
    )
    await state.clear()


async def change_percent_callback(callback: CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text(
        "Enter percentage change for tracking:", reply_markup=INLINE_BACK_TO_TRACK_PRICES_KB
    )
    await state.set_state(TrackPairs.change_percent)
    await state.update_data(message_id=message.message_id)


async def change_percent(message: Message, state: FSMContext, user: User, repository: Repository):
    try:
        new_percent = Decimal(message.text)
        if not 1 <= new_percent <= 1000:
            raise ValueError
    except ValueError:
        return await message.answer("Please enter a number from 1 to 1000!")

    await services.change_percent(user, new_percent, repository.user)
    await message.answer(f"Current percent: {new_percent.normalize():g}%")
    await edit_or_send_message_by_id(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=(await state.get_data())["message_id"],
        text=get_tracking_bar_message(user.percent, user.pairs),
        reply_markup=INLINE_TRACK_PRICES_KB,
    )
    await state.clear()


async def back_to_track_prices_callback(callback: CallbackQuery, state: FSMContext, user: User):
    await state.clear()
    await show_track_prices_panel_callback(callback, user)


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(add_pair, StateFilter(TrackPairs.add_pair), F.content_type == ContentType.TEXT)
    router.message.register(remove_pair, StateFilter(TrackPairs.remove_pair), F.content_type == ContentType.TEXT)
    router.message.register(change_percent, StateFilter(TrackPairs.change_percent), F.content_type == ContentType.TEXT)
    router.callback_query.register(show_track_prices_panel_callback, F.data == "track_prices")
    router.callback_query.register(add_pair_callback, F.data == "add_pair")
    router.callback_query.register(remove_pair_callback, F.data == "remove_pair")
    router.callback_query.register(change_percent_callback, F.data == "change_percent")
    router.callback_query.register(back_to_track_prices_callback, F.data == "back_to_track_prices")
    return router
