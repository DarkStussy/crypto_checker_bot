import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.api.gateways import Gateway
from keyboard.inline import inline_kb_track_prices, inline_kb_close
from states.search_pairs import TrackPairs
from utils.functions import get_all_pairs, get_price_of_pairs


async def track_prices(callback_query: types.CallbackQuery, gateway: Gateway):
    user = await gateway.user.get_by_chat_id(callback_query.message.chat.id)
    await callback_query.message.edit_text(f'<b>Percentage Change:</b> {user.percent}%\n'
                                           f'<b>Current tracking pairs:</b>\n'
                                           f'<i>{", ".join(user.crypto_pairs)}</i>',
                                           reply_markup=inline_kb_track_prices,
                                           parse_mode=types.ParseMode.HTML)


async def add_pair(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_close, parse_mode=types.ParseMode.HTML)
    await TrackPairs.add_pair.set()


async def remove_pair(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_close, parse_mode=types.ParseMode.HTML)
    await TrackPairs.remove_pair.set()


async def inline_search_pairs(inline_query: types.InlineQuery, state: FSMContext):
    async with state.proxy() as data:
        pairs = data.get('pairs')
        if pairs is None:
            pairs = await get_all_pairs()
            data['pairs'] = pairs

        text = inline_query.query or 'BTCUSDT'
        if text != 'BTCUSDT':
            search_list = data.get(text)
            query_offset = int(inline_query.offset) if inline_query.offset else 0
            if search_list is None:
                search_list = tuple(pair for pair in pairs if text in pair)
                data[text] = search_list

            results = [types.InlineQueryResultArticle(
                id=pair,
                title=pair,
                input_message_content=types.InputTextMessageContent(
                    message_text=pair
                )
            ) for pair in search_list if text in pair]
            if len(results) < 50:
                await inline_query.answer(results, is_personal=True, next_offset="",
                                          cache_time=10)
            else:
                await inline_query.answer(results[query_offset:query_offset + 50], is_personal=True,
                                          next_offset=str(query_offset + 50),
                                          cache_time=10)
        else:
            item = types.InlineQueryResultArticle(
                id=text,
                title=text,
                input_message_content=types.InputTextMessageContent(
                    message_text=text
                ))
            await inline_query.answer([item], is_personal=True, cache_time=10)


async def enter_and_add_pair(message: types.Message, gateway: Gateway, state: FSMContext):
    new_pair = message.text
    price = (await get_price_of_pairs([new_pair]))[0]
    if price is None:
        return await message.answer('Pair does not exist')

    user = await gateway.user.get_by_chat_id(message.chat.id)
    if user:
        if new_pair in user.crypto_pairs:
            return await message.answer('The pair is tracking at the moment!')
        try:
            user.crypto_pairs.append(new_pair)
            await gateway.merge(user)
        except Exception as e:
            logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
            await state.finish()
            return await message.answer('There were some problems, please try again later.')
    else:
        user = await gateway.user.create_new_user(message.chat.id, [message.text])

    await message.answer(f'Tracking of this cryptocurrency pair has successfully started!\n'
                         f'<b>{new_pair}</b>: {float(price):g}\n\n'
                         f'<b>Current tracking pairs:</b>\n'
                         f'<i>{", ".join(user.crypto_pairs)}</i>', reply_markup=inline_kb_close,
                         parse_mode=types.ParseMode.HTML)
    await state.finish()


async def enter_and_remove_pair(message: types.Message, gateway: Gateway, state: FSMContext):
    new_pair = message.text
    user = await gateway.user.get_by_chat_id(message.chat.id)
    if user:
        try:
            user.crypto_pairs.remove(new_pair)
            await gateway.merge(user)
        except ValueError:
            return await message.answer('This pair is not in your list of tracking pairs!')
        except Exception as e:
            logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
            await message.answer('There were some problems, please try again later.')
        else:
            await message.answer(f'Pair has successfully deleted\n\n'
                                 f'<b>Currently tracked pairs:</b>\n'
                                 f'<i>{", ".join(user.crypto_pairs)}</i>', reply_markup=inline_kb_close,
                                 parse_mode=types.ParseMode.HTML)
    else:
        await message.answer('List of tracking pairs is empty...')

    await state.finish()


async def change_percent(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Enter percentage change in tracking:', reply_markup=inline_kb_close)
    await TrackPairs.change_percent.set()


async def enter_percent(message: types.Message, gateway: Gateway, state: FSMContext):
    try:
        percent = float(message.text)
        if percent <= 0:
            raise ValueError
    except ValueError:
        await message.answer('Please enter a positive floating point number!')
    else:
        user = await gateway.user.get_by_chat_id(message.chat.id)
        user.percent = percent
        await gateway.merge(user)
        await message.answer(f'Current percent: {percent:g}%')
        await state.finish()


def register_track_prices(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(enter_and_add_pair, state=TrackPairs.add_pair, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(enter_and_remove_pair, state=TrackPairs.remove_pair,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(enter_percent, state=TrackPairs.change_percent, content_types=types.ContentTypes.TEXT)

    # callback handlers
    dp.register_callback_query_handler(track_prices, Text('track_prices'))
    dp.register_callback_query_handler(add_pair, Text('add_pair'))
    dp.register_callback_query_handler(remove_pair, Text('remove_pair'))
    dp.register_callback_query_handler(change_percent, Text('change_percent'))

    # inline handlers
    dp.register_inline_handler(inline_search_pairs, state=[TrackPairs.add_pair, TrackPairs.remove_pair])
