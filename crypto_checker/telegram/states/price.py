from aiogram.fsm.state import StatesGroup, State


class CheckPrice(StatesGroup):
    pair = State()
