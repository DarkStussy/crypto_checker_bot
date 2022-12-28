import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiohttp import ClientSession

from database.api.gateways import Gateway
from keyboard.inline import inline_kb_track_prices, inline_kb_close, inline_kb_back_to_check_prices
from states.search_pairs import TrackPairs
from utils.functions import get_price_of_pairs


async def track_prices(callback_query: types.CallbackQuery, gateway: Gateway):
    user = await gateway.user.get_by_chat_id(callback_query.message.chat.id)
    message_text = 'Tracking bar:'
    if user:
        pairs_str = ', '.join(user.crypto_pairs)
        message_text = f'<b>Percentage Change:</b> {user.percent}%\n\n<b>Current tracking pairs:</b>\n<i>' \
                       f'{pairs_str if pairs_str else "-"}</i>'
    await callback_query.message.edit_text(message_text,
                                           reply_markup=inline_kb_track_prices,
                                           parse_mode=types.ParseMode.HTML)


async def add_pair(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter cryptocurrency pair.\n'
                                           f'Use <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_back_to_check_prices, parse_mode=types.ParseMode.HTML)
    await TrackPairs.add_pair.set()


async def remove_pair(callback_query: types.CallbackQuery):
    bot = await callback_query.bot.get_me()
    await callback_query.message.edit_text(f'Enter cryptocurrency pair.\n'
                                           f'Use <code>@{bot.username}</code> to view all pairs',
                                           reply_markup=inline_kb_back_to_check_prices, parse_mode=types.ParseMode.HTML)
    await TrackPairs.remove_pair.set()


async def enter_and_add_pair(message: types.Message, gateway: Gateway, client_session: ClientSession,
                             state: FSMContext):
    new_pair = message.text.upper()
    price = (await get_price_of_pairs(client_session, [new_pair]))[0]
    try:
        price = float(price)
    except (ValueError, TypeError):
        await message.answer('There were some problems, please try again later.')
    else:
        user = await gateway.user.get_by_chat_id(message.chat.id)
        if user:
            if new_pair in user.crypto_pairs:
                return await message.answer('The pair is tracking at the moment!')
            elif len(user.crypto_pairs) >= 50:
                await state.finish()
                return await message.answer('Max 50 pairs can be tracking')
            try:
                user.crypto_pairs[new_pair] = price
                await gateway.merge(user)
            except Exception as e:
                logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
                await state.finish()
                return await message.answer('There were some problems, please try again later.')
        else:
            user = await gateway.user.create(message.chat.id, {new_pair: price})

        pairs_str = ', '.join(user.crypto_pairs)
        await message.answer(f'Tracking of this cryptocurrency pair has successfully started!\n'
                             f'<b>{new_pair}</b>: {float(price):g}\n\n'
                             f'<b>Current tracking pairs:</b>\n'
                             f'<i>{pairs_str if pairs_str else "-"}</i>', reply_markup=inline_kb_close,
                             parse_mode=types.ParseMode.HTML)
    await state.finish()


async def enter_and_remove_pair(message: types.Message, gateway: Gateway, state: FSMContext):
    new_pair = message.text.upper()
    user = await gateway.user.get_by_chat_id(message.chat.id)
    if user:
        try:
            del user.crypto_pairs[new_pair]
            await gateway.merge(user)
        except KeyError:
            return await message.answer('This pair is not in your list of tracking pairs!')
        except Exception as e:
            logging.error(f'Error: {type(e).__name__}, file: {__file__}, line: {e.__traceback__.tb_lineno}')
            await message.answer('There were some problems, please try again later.')
        else:
            pairs_str = ', '.join(user.crypto_pairs)
            await message.answer(f'Pair has successfully deleted\n\n'
                                 f'<b>Currently tracked pairs:</b>\n'
                                 f'<i>{pairs_str if pairs_str else "-"}</i>', reply_markup=inline_kb_close,
                                 parse_mode=types.ParseMode.HTML)
    else:
        await message.answer('List of tracking pairs is empty...')

    await state.finish()


async def change_percent(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Enter percentage change in tracking:',
                                           reply_markup=inline_kb_back_to_check_prices)
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
        await message.answer(f'Current percent: {percent:g}%', reply_markup=inline_kb_close)
        await state.finish()


async def back_to_check_prices(callback_query: types.CallbackQuery, gateway: Gateway, state: FSMContext):
    await state.finish()
    await track_prices(callback_query, gateway)


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
    dp.register_callback_query_handler(back_to_check_prices, Text('back_to_check_prices'), state='*')
