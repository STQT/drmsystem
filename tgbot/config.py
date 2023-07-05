from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class DbConfig:
    database_url: str
    admin_login: str
    admin_password: str
    secret_key: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


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
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            database_url=env.str('DATABASE_URL'),
            admin_login=env.str('DB_ADMIN_LOGIN'),
            admin_password=env.str('DB_ADMIN_PASSWORD'),
            secret_key=env.str("DB_ADMIN_SECRET_KEY")
        ),
        misc=Miscellaneous(
            payme=env.str('PAYME'),
            click=env.str('CLICK'),
            sentry_sdk=env.str('SENTRY_SDK'),
            sms_url=env.str('SMS_URL'),
            sms_login=env.str('SMS_LOGIN'),
            sms_pass=env.str('SMS_PASS')
        )
    )


I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
