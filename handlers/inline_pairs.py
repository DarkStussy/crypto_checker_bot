from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession

from states.check_price import CheckPrice
from states.track_pairs import TrackPairs
from utils.functions import get_all_pairs


async def inline_search_pairs(inline_query: types.InlineQuery,
                              client_session: ClientSession,
                              state: FSMContext):
    data = await state.get_data()
    pairs = data.get('pairs')
    if pairs is None:
        pairs = await get_all_pairs(client_session)
        await state.update_data(pairs=pairs)

    text = inline_query.query or 'BTCUSDT'
    if text != 'BTCUSDT':
        search_list = data.get(text)
        query_offset = int(inline_query.offset) if inline_query.offset else 0
        if search_list is None:
            search_list = tuple(pair for pair in pairs if text in pair)
            data[text] = search_list
            await state.update_data({'text': search_list})

        results = [types.InlineQueryResultArticle(
            id=pair,
            title=pair,
            input_message_content=types.InputTextMessageContent(
                message_text=pair
            )
        ) for pair in search_list if text in pair]
        if len(results) < 50:
            await inline_query.answer(results, is_personal=True,
                                      next_offset='',
                                      cache_time=10)
        else:
            await inline_query.answer(results[query_offset:query_offset + 50],
                                      is_personal=True,
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


def register_inline_pairs(dp: Dispatcher):
    # inline handlers
    dp.register_inline_handler(inline_search_pairs,
                               state=[TrackPairs.add_pair,
                                      TrackPairs.remove_pair,
                                      CheckPrice.cryptocurrency])
