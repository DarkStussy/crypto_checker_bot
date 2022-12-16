from aiogram import Dispatcher

from handlers.get_price import register_get_price
from handlers.menu import register_menu
from handlers.track_prices import register_track_prices
from handlers.unknown_messages import register_unknown_message


def setup_handlers(dp: Dispatcher):
    register_menu(dp)
    register_get_price(dp)
    register_track_prices(dp)

    # last handlers
    register_unknown_message(dp)
