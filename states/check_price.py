from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckPrice(StatesGroup):
    cryptocurrency = State()
