from envparse import env
from sqlalchemy.util import EMPTY_DICT

from .models import Config, BotConfig, DbConfig, SchedulerConfig


def load_config() -> Config:
    return Config(
        bot=BotConfig(
            token=env.str("BOT_TOKEN"), admins=list(map(int, env.list("ADMINS"))),
        ),
        db=(
            DbConfig.from_url(
                url,
                type_=env.str("DB_TYPE", default="postgresql"),
                connector=env.str("DB_CONNECTOR", default="asyncpg"),
                query=env.dict("DB_QUERY", default=EMPTY_DICT),
            )
            if (url := env.str("DATABASE_URL")) is not None
            else DbConfig(
                type=env.str("DB_TYPE", default="postgresql"),
                connector=env.str("DB_CONNECTOR", default="asyncpg"),
                host=env.str("DB_HOST", default="localhost"),
                port=env.int("DB_PORT", default=5432),
                username=env.str("DB_USERNAME"),
                password=env.str("DB_PASSWORD"),
                database=env.str("DB_DATABASE"),
                query=env.dict("DB_QUERY", default=EMPTY_DICT),
            )
        ),
        scheduler=SchedulerConfig(
            interval=env.int("SCHEDULER_INTERVAL", default=5),
            max_instances=env.int("SCHEDULER_MAX_INSTANCES", default=1),
        ),
    )
