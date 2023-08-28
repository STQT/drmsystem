import asyncio
import logging

from datetime import datetime, timedelta

import aiohttp
from aiogram import Bot
from aiogram.types import Message
from aiogram.utils import exceptions

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.keyboards.inline import prices_keyboard
from tgbot.keyboards.reply import main_menu_keyboard
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def update_server_photo_uri(db: Database, org_slug, file_id):
    await db.update_organization(org_slug, {
        "photo_uri": file_id,
        "photo_updated": False
    })


async def send_answer_organization(m: Message, db: Database, org_slug, config: Config,
                                   callback_query=None):
    if callback_query:
        await callback_query.message.delete()
    org = await db.get_organization_obj(org_slug)
    org = org[0]
    if org is None:
        org = await db.get_organization_obj("main")
        org = org[0]
    prices = await db.get_prices()
    caption = (f"{org['name']}\n"
               "Жазылым бағасын таңдаңыз")
    reply_markup = prices_keyboard(prices[0])
    photo_uri = org.get("photo_uri", "error")
    if not org["photo_uri"] or org["photo_updated"] is True:
        url = org['photo']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    photo_resp = await m.answer_photo(photo=image_bytes, reply_markup=reply_markup, caption=caption)
                    await update_server_photo_uri(db, org_slug=org['slug'], file_id=photo_resp.photo[-1].file_id)
    else:
        try:
            await m.answer_photo(photo_uri, reply_markup=reply_markup, caption=caption)
        except exceptions.WrongFileIdentifier:
            photo_resp = await m.answer_photo(org['photo'], reply_markup=reply_markup, caption=caption)
            await update_server_photo_uri(db, org_slug=org['slug'], file_id=photo_resp.photo[-1].file_id)
    return org['slug']


async def create_invite_link(bot: Bot, channel_id, name):
    expire_date = datetime.now() + timedelta(days=1)
    invite_link = await bot.create_chat_invite_link(chat_id=channel_id,
                                                    expire_date=expire_date,
                                                    member_limit=1,
                                                    name=name)
    return invite_link.invite_link


async def broadcast_send_message(m: Message, user_id, db: Database, disable_notification: bool = False) -> bool:
    try:
        await m.send_copy(user_id, disable_notification=disable_notification, reply_markup=main_menu_keyboard())
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await broadcast_send_message(m, user_id, db)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    await db.update_user(user_id, {"stopped": True})
    return False


async def get_user_per_page(db: Database, page=1):
    users_json = await db.get_users_by_pagination(page)
    if users_json[1] != 200:
        return [], False
    results = users_json[0]["results"]
    have_next_page = True if users_json[0]["count"] > (page * 100) else False
    return results, have_next_page


async def broadcaster(m: Message, db: Database) -> int:
    count = 0
    page = 1

    have_next = True
    while have_next is True:
        all_users, have_next = await get_user_per_page(db, page=page)
        try:
            for user in all_users:
                if await broadcast_send_message(m, user['id'], db):
                    count += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        finally:
            logging.info(f"{count} messages successful sent.")
        page += 1

    return count
