import re

from datetime import datetime, timedelta

import aiohttp
from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.exceptions import WrongFileIdentifier

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.keyboards.inline import prices_keyboard
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
        except WrongFileIdentifier:
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
