import re
import logging

from aiogram import types
from aiogram.types import Message

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.db.redis_db import get_redis, get_user_shopping_cart, get_cart_items_text, get_cart_items_list
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
                "Jami: {cost} so'm"
            ).format(
                cart_items_text=cart_items_text,
                total_price=total_price,
                cost=total_price
            ),
            reply_markup=shopping_cart_kb())


def collect_data_for_request(data, cart_items, user_lang, check_id=None):
    order_data = {
        "address": data["address"].replace("'", "´").replace('"', "”"),
        "check_id": check_id if check_id else "Naqd pul",
        "phone": data["contact"],
        "payment_method": data["payment_method"],
        "cost": data["cost"],
    }
    product_list: list[dict] = get_cart_items_list(cart_items)
    items_list = []
    for item in product_list:
        items_list.append({
            "product_lang": user_lang,
            "product_name": item["name"].replace("'", "´").replace('"', "”"),
            "count": item["count"]
        })
    order_data.update({"products": items_list})
    return order_data


async def update_server_photo_uri(db: Database, product_id, file_id):
    await db.update_product(product_id, {
        "photo_uri": file_id,
        "photo_updated": False
    })


async def send_to_group_order(m: Message, config: Config, data, cart_items_text, total_price, db: Database):
    await m.bot.send_message(
        config.tg_bot.group_id,
        _(
            "Yangi buyurtma:\n"
            "Manzil: {address}\n\n"
            "{cart_items_text}\n"
            "To'lov turi: {payment_method}\n\n"
            "Mahsulotlar: {total_price} so'm\n"
            "Telefon raqam: {phone}\n"
            "Jami: {cost} so'm"
        ).format(
            address=data["address"],
            payment_method=data["payment_method"],
            cart_items_text=cart_items_text,
            total_price=total_price,
            phone=data['contact'],
            cost=total_price
        ))


def validate_uzbek_phone_number(number):
    # Regular expression pattern for Uzbekistan phone numbers
    pattern = r'^\+998 \d{2} \d{3} \d{2} \d{2}$'

    # Check if the number matches the pattern
    if re.match(pattern, number):
        return True
    else:
        return False
