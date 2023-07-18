import logging

from aiogram import types

from tgbot.db.queries import Database
from tgbot.db.redis_db import get_redis, get_user_shopping_cart, get_cart_items_text
from tgbot.keyboards.inline import shopping_cart_kb
from tgbot.keyboards.reply import address_clear, back_button, locations_buttons
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def get_my_location_text(m: types.Message, user_lang, db: Database, remove_button=True):
    locations = await db.get_user_locations(m.from_user.id)
    if locations:
        loc_str = ""
        for num, location in enumerate(locations):
            loc_str += str(num + 1) + ". " + location['name'] + "\n"
        await m.answer(loc_str)
        await m.answer(_("O'z manzillaringizni tozalamoqchimisiz?"),
                       reply_markup=address_clear())
    else:
        await m.answer(_("Manzillar mavjud emas"), reply_markup=back_button(locale=user_lang))


async def get_my_location_for_select(m: types.Message, user_lang, db: Database):
    locations = await db.get_user_locations(m.from_user.id)
    if locations:
        await m.answer(_("Yetkazib berish manzilni tanlang"), reply_markup=locations_buttons(locations))
    else:
        await m.answer(_("Manzillar mavjud emas"), reply_markup=back_button(locale=user_lang))


async def get_shopping_cart(m: types.Message, db: Database):
    cart_items = await get_user_shopping_cart(m.from_user.id)
    if not cart_items:
        await m.answer(_("Savat bo'sh"))
    else:
        cart_items_text, total_price = get_cart_items_text(cart_items)
        await m.answer(
            _(
                "Savatda:\n"
                "{cart_items_text}"
                "Mahsulotlar: {total_price} so'm\n"
                "Yetkazib berish: {delivery} so'm\n"
                "Jami: {cost} so'm"
            ).format(
                cart_items_text=cart_items_text,
                total_price=total_price,
                delivery=db.DELIVERY_COST,
                cost=int(db.DELIVERY_COST) + total_price
            ),
            reply_markup=shopping_cart_kb())