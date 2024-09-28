import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .tracking import check_users_pairs
from ..config import SchedulerConfig
from ..infrastructure.binance import BinanceClient
from ..infrastructure.db.provider import DbProvider


def run_scheduler(bot: Bot, db_provider: DbProvider, binance_client: BinanceClient, config: SchedulerConfig):
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_users_pairs,
        trigger="interval",
        args=(bot, db_provider, binance_client),
        seconds=config.interval,
        max_instances=config.max_instances,
    )
    scheduler.start()
