from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from crypto_checker.core.models.dto import User
from crypto_checker.infrastructure.binance import BinanceClient
from ..keyboards.inline import INLINE_BACK_TO_MENU_KB
from ..states.price import CheckPrice
from ...utils.messages import get_prices_changes_message


async def check_prices(message: Message, user: User, binance_client: BinanceClient):
    if not user.pairs:
        return await message.answer("List of tracking pairs is empty")

    pairs = await binance_client.get_pairs_price([pair.name for pair in user.pairs])
    if not pairs:
        return await message.answer("Failed to get pricing information :(")

    if msg := get_prices_changes_message(user.pairs, pairs):
        await message.answer(msg)


async def get_price_callback(callback: CallbackQuery, state: FSMContext):
    bot = await callback.bot.get_me()
    await callback.message.edit_text(
        f"Enter cryptocurrency pair.\nUse <code>@{bot.username}</code> to view all pairs",
        reply_markup=INLINE_BACK_TO_MENU_KB,
    )
    await state.set_state(CheckPrice.pair)


async def get_price_command(message: Message, state: FSMContext):
    bot = await message.bot.get_me()
    await message.answer(
        f"Enter cryptocurrency pair.\nUse <code>@{bot.username}</code> to view all pairs",
        reply_markup=INLINE_BACK_TO_MENU_KB,
    )
    await state.set_state(CheckPrice.pair)


async def get_price(message: Message, state: FSMContext, binance_client: BinanceClient):
    pair_name = str(message.text.upper())
    pairs = await binance_client.get_pairs_price([pair_name])
    price = pairs.get(pair_name)
    if price is None:
        return await message.answer(f"Price of {pair_name} not found")

    await message.answer(f"<b>{pair_name} price:</b> <i>{price:f}</i>")
    await state.clear()


async def show_pairs(inline: InlineQuery, binance_client: BinanceClient):
    pairs = await binance_client.get_all_pairs()
    query = inline.query.strip().upper()
    if len(query) < 2:
        return

    limit = 20
    query_offset = int(inline.offset) if inline.offset else 0
    results = [
        InlineQueryResultArticle(
            id=pair,
            title=pair,
            input_message_content=InputTextMessageContent(message_text=pair),
        )
        for pair in pairs
        if query in pair
    ]
    if not results:
        return

    if len(results) <= limit:
        return await inline.answer(results, is_personal=True, next_offset="", cache_time=10)

    await inline.answer(
        results[query_offset : query_offset + limit],
        is_personal=True,
        next_offset=str(query_offset + limit),
        cache_time=10,
    )


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(check_prices, Command("check"))
    router.message.register(get_price, StateFilter(CheckPrice.pair), F.content_type == ContentType.TEXT)
    router.message.register(get_price_command, Command("get_price"))
    router.callback_query.register(get_price_callback, F.data == "get_price")
    router.inline_query.register(show_pairs)
    return router
