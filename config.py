import os

from dotenv import load_dotenv

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    password: str
    username: str
    database: str


@dataclass
class BotConfig:
    token: str
    admins: tuple[int]
    use_redis: bool


@dataclass
class Config:
    bot: BotConfig
    db: DatabaseConfig


def load_config():
    load_dotenv()

    return Config(bot=BotConfig(
        token=os.getenv('BOT_TOKEN'),
        admins=(12345,),  # admins id here
        use_redis=True),
        db=DatabaseConfig(
            host=os.getenv('PG_HOST'),
            password=os.getenv('PG_PASSWORD'),
            username=os.getenv('PG_USERNAME'),
            database=os.getenv('PG_DATABASE')
        )
    )
