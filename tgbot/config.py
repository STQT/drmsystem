import logging
from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class DbConfig:
    base_url: str


@dataclass
class TgBot:
    debug: bool
    token: str
    admin_ids: list[int]
    group_id: str
    channel_id: str

@dataclass
class Miscellaneous:
    sentry_dsn: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            debug=env.bool("BOT_DEBUG"),
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            group_id=env.str("GROUP_ID"),
            channel_id=env.str("CHANNEL_ID"),
        ),
        db=DbConfig(
            base_url=env.str("API_BASE_URL")
        ),
        misc=Miscellaneous(
            sentry_dsn=env.str('BOT_SENTRY_DSN'),
        )
    )


I18N_DOMAIN = 'mybot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
