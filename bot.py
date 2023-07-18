import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.db.queries import Database
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.callback_query import register_callback
from tgbot.handlers.echo import register_echo
from tgbot.handlers.main_menu import register_menu
from tgbot.handlers.review import register_review
from tgbot.handlers.settings import register_settings
from tgbot.handlers.user_start import register_user
from tgbot.middlewares.acl import ACLMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.i18n import i18ns

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, db):
    dp.setup_middleware(EnvironmentMiddleware(config=config, db=db))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(i18ns)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_review(dp)
    register_menu(dp)
    register_settings(dp)
    register_callback(dp)

    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(host="redis", port=6380, db=0)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    logging.info(config)
    bot['config'] = config

    register_all_middlewares(dp, config,
                             db=Database(config.db.base_url))
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
