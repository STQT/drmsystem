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


@dataclass
class Miscellaneous:
    payme: str
    click: str
    sentry_sdk: str
    sms_url: str
    sms_login: str
    sms_pass: str


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
        ),
        db=DbConfig(
            base_url=env.str("API_BASE_URL")
        ),
        misc=Miscellaneous(
            payme=env.str('PAYME'),
            click=env.str('CLICK'),
            sentry_sdk=env.str('BOT_SENTRY_SDK'),
            sms_url=env.str('SMS_URL'),
            sms_login=env.str('SMS_LOGIN'),
            sms_pass=env.str('SMS_PASS')
        )
    )


I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
