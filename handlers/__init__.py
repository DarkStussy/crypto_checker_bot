from aiogram import Dispatcher

from handlers.check_prices import register_check_prices
from handlers.get_price import register_get_price
from handlers.inline_pairs import register_inline_pairs
from handlers.menu import register_menu
from handlers.track_prices import register_track_prices
from handlers.unknown_messages import register_unknown_message


def setup_handlers(dp: Dispatcher):
    register_menu(dp)
    register_inline_pairs(dp)
    register_get_price(dp)
    register_track_prices(dp)
    register_check_prices(dp)

    # last handlers
    register_unknown_message(dp)
