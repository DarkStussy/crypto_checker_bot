from aiogram.dispatcher import FSMContext


async def get_data_from_state(state: FSMContext, key):
    async with state.proxy() as data:
        return data.get(key, None)


async def set_data_state(state: FSMContext, **data):
    async with state.proxy() as state_data:
        for key, value in data.items():
            state_data[key] = value
