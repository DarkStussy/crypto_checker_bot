from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('menu', 'Show menu'),
        types.BotCommand('check', 'Check changes since last tracking'),
    ])
