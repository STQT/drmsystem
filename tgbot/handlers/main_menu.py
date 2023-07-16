import logging
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from urllib.parse import urlparse

from tgbot.db.queries import Database
from tgbot.keyboards.inline import product_inline_kb
from tgbot.keyboards.reply import settings_buttons, menu_keyboards, get_verification, \
    generate_category_keyboard, generate_product_keyboard, only_cart_and_back_btns
from tgbot.misc.geolocation import get_location_name_async
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import MainMenuState, SettingsState, BuyState
from tgbot.misc.utils import get_my_location_for_select

_ = i18ns.gettext


async def main_menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.text == _("Menyu", locale=user_lang):
        await m.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                       reply_markup=menu_keyboards())
        await BuyState.get_location.set()

    elif m.text == _("Izoh qoldirish", locale=user_lang):
        await m.answer("Izoh qoldirish")
    elif m.text == _("Sozlamalar", locale=user_lang):
        await m.answer("Sozlamalar", reply_markup=settings_buttons())
        await SettingsState.get_buttons.set()
    else:
        await m.answer(_("Mavjud bo'lmagan buyruq!"))


async def menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.content_type in (types.ContentType.TEXT,):
        if m.text == _("🗺 Mening manzilim"):
            await get_my_location_for_select(m, user_lang, db)
            return
        if m.text == _("✅ Ha"):
            data = await state.get_data()
            # SEND TO DB NEW ADDRESS AND SHOW CATEGORIES
            resp_data = await db.create_user_location(
                user_id=m.from_user.id,
                longitude=data['longitude'],
                latitude=data['latitude'],
                address=data['address']
            )
            if resp_data:
                await state.update_data(address=data['address'])
                categories = await db.get_categories()
                await m.answer(_("Muzqaymoq turini tanlang."),
                               reply_markup=generate_category_keyboard(categories, user_lang))
                await BuyState.get_category.set()
            else:
                await m.answer(_("Server bilan bog'lanishda muammo qaytadan urunib ko'ring"))
        elif m.text in (_("❌ Yo'q"), _("⬅️ Ortga")):
            await m.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                           reply_markup=menu_keyboards())
            await BuyState.get_location.set()
        else:
            categories = await db.get_categories()
            await state.update_data(address=m.text)
            await m.answer(_("Bo'limni tanlang."),
                           reply_markup=generate_category_keyboard(categories, user_lang))

            await BuyState.get_category.set()

    ################################################################
    else:
        # GET longitude and latitude. Request pygis geolocation
        location = m.location
        address = await get_location_name_async(location.latitude, location.longitude)
        await state.update_data(longitude=location.longitude,
                                latitude=location.latitude,
                                address=address)
        await m.answer(
            _("Buyurtma bermoqchi bo'lgan manzil:\n"
              f"{address}\n"
              "Ushbu manzilni tasdiqlaysizmi?").format(address=address),
            reply_markup=get_verification()
        )


async def get_category(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("⬅️ Ortga"): # noqa
        await m.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                       reply_markup=menu_keyboards())
        await BuyState.get_location.set()
        return
    await state.update_data(
        category=m.text)
    products = await db.get_products(category=m.text, user_lang=user_lang)
    # TODO: rasm kerakmi?
    await m.answer(_("Muzqaymoqni tanlang"), reply_markup=generate_product_keyboard(products, user_lang))
    await BuyState.get_product.set()


async def get_product(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("⬅️ Ortga"): # noqa
        categories = await db.get_categories()
        await m.answer(_("Muzqaymoq turini tanlang."),
                       reply_markup=generate_category_keyboard(categories, user_lang))
        await BuyState.get_category.set()
        return
    await state.update_data(
        category=m.text)
    product = await db.get_product(m.text, user_lang)
    if product:
        await m.answer(_("Quyidagilardan birini tanlang"), reply_markup=only_cart_and_back_btns())
        url = product['photo']
        parsed_url = urlparse(url)
        file_name: str = parsed_url.path.split("/")[-1] # noqa
        with open("api/media/" + file_name, "rb") as file:
            await m.answer_photo(
                photo=file,
                reply_markup=product_inline_kb()
            )
    else:
        await m.answer(_("Iltimos ro'yxatdagi maxsulotni tanlang"))


# async def get_user_location(m: Message, state: FSMContext, user_lang):
#     await state.update_data(longitude=m.location.longitude,
#                             latitude=m.location.latitude)
#     await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_keyboard(user_lang))
#     data = await state.get_data()
#     logging.info(data)
#     await state.finish()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, state=MainMenuState.get_menu)
    dp.register_message_handler(menu, content_types=["text", "location"], state=BuyState.get_location)
    dp.register_message_handler(get_category, state=BuyState.get_category)
    dp.register_message_handler(get_product, state=BuyState.get_product)
