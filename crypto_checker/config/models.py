from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import make_url, URL


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

    @classmethod
    def from_url(cls, url: str, type_: str, connector: str, query: dict[str, Sequence[str] | str]) -> "DbConfig":
        url = make_url(url)
        return cls(
            type=type_,
            connector=connector,
            host=url.host,
            port=url.port,
            username=url.username,
            password=url.password,
            database=url.database,
            query=query,
        )

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=f"{self.type}+{self.connector}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=self.query,
        )


@dataclass(slots=True, frozen=True)
class BotConfig:
    token: str
    admins: list[int]


@dataclass(slots=True, frozen=True)
class Config:
    bot: BotConfig
    db: DbConfig
    scheduler: SchedulerConfig
