from aiogram import Bot


async def notify_admins(bot: Bot, admins: list[int]):
    for admin in admins:
        await bot.send_message(admin, "Bot started")
