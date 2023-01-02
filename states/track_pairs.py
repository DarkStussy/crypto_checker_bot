from aiogram.dispatcher.filters.state import StatesGroup, State


class TrackPairs(StatesGroup):
    add_pair = State()
    remove_pair = State()
    change_percent = State()
