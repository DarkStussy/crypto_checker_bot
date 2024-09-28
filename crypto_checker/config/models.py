from dataclasses import dataclass
from typing import Sequence


@dataclass(slots=True, frozen=True)
class SchedulerConfig:
    interval: int
    max_instances: int


@dataclass(slots=True, frozen=True)
class DbConfig:
    type: str
    connector: str
    host: str
    port: int
    username: str
    password: str
    database: str
    query: dict[str, Sequence[str] | str]


@dataclass(slots=True, frozen=True)
class BotConfig:
    token: str
    admins: list[int]


@dataclass(slots=True, frozen=True)
class Config:
    bot: BotConfig
    db: DbConfig
    scheduler: SchedulerConfig
