from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentTypes
from urllib.parse import urlparse

from aiogram.utils.exceptions import WrongFileIdentifier

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.db.redis_db import get_redis, get_user_shopping_cart, get_cart_items_text, get_cart_items_list, \
    clear_user_shopping_cart
from tgbot.keyboards.inline import product_inline_kb, shopping_cart_kb
from tgbot.keyboards.reply import settings_buttons, menu_keyboards, get_verification, \
    generate_category_keyboard, generate_product_keyboard, only_cart_and_back_btns, main_menu_keyboard, \
    payment_method_btns, get_contact_keyboard, approve_btns, cancel_btn
from tgbot.misc.geolocation import get_location_name_async
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import MainMenuState, SettingsState, BuyState, ReviewState
from tgbot.misc.utils import get_my_location_for_select, get_shopping_cart, collect_data_for_request, \
    validate_uzbek_phone_number
from tgbot.misc.utils import get_my_location_for_select, get_shopping_cart, collect_data_for_request, \
    update_server_photo_uri, send_to_group_order

_ = i18ns.gettext


async def main_menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.text == _("Menyu", locale=user_lang):
        await m.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                       reply_markup=menu_keyboards())
        await BuyState.get_location.set()

    elif m.text == _("Izoh qoldirish", locale=user_lang):
        await m.answer(_("Izohingizni yuboring\n"
                         "(Video, Audio, Xat"), reply_markup=cancel_btn())
        await ReviewState.get_review.set()
    elif m.text == _("Sozlamalar", locale=user_lang):
        await m.answer("Sozlamalar", reply_markup=settings_buttons())
        await SettingsState.get_buttons.set()
    else:
        await m.answer(_("Mavjud bo'lmagan buyruq!"))
        await state.finish()


async def menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.content_type in (types.ContentType.TEXT,):
        if m.text == _("⬅️ Ortga"):
            await m.answer(_("Bo'limni tanlang", locale=user_lang),
                           reply_markup=main_menu_keyboard(user_lang))
            await MainMenuState.get_menu.set()
            return
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
    if m.text == _("⬅️ Ortga"):  # noqa
        await m.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                       reply_markup=menu_keyboards())
        await BuyState.get_location.set()
        return
    elif m.text == _("📥 Savat"):
        await get_shopping_cart(m, db)
        return
    await state.update_data(category=m.text)
    products = await db.get_products(category=m.text, user_lang=user_lang)
    # TODO: rasm kerakmi?
    await m.answer(_("Muzqaymoqni tanlang"), reply_markup=generate_product_keyboard(products, user_lang))
    await BuyState.get_product.set()


async def get_product(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("⬅️ Ortga"):  # noqa
        categories = await db.get_categories()
        await m.answer(_("Muzqaymoq turini tanlang."),
                       reply_markup=generate_category_keyboard(categories, user_lang))
        await BuyState.get_category.set()
        return
    elif m.text == _("📥 Savat"):
        await get_shopping_cart(m, db)
        return

    product = await db.get_product(m.text, user_lang)
    if product:
        await m.answer(_("Muzqaymoq sonini ko'rsating"), reply_markup=only_cart_and_back_btns())
        await state.update_data(product=m.text, price=product['price'])
        photo_uri = product.get("photo_uri")
        caption = _("💲 Narxi: {price}\n"
                    "⚖️ Og'irligi: {massa}\n"
                    "🧈 Yog' miqdori: {jirnost}\n"
                    "🌡 Saqlash harorati: {temperature}\n"
                    "📅 Saqlash muddati: {srok_godnosti}\n"
                    "📦 Qadolati: {upakovka}\n"
                    "🧪 Protein: {protein}\n"
                    "🧪 Fat: {fat}\n"
                    "🧪 Carbohydrate: {carbohydrate}\n"
                    "🧪 Calories: {calories}\n"
                    ).format(
            price=product['price'],
            massa=product['massa'],
            jirnost=product['jirnost'],
            temperature=product['temperature'],
            srok_godnosti=product['srok_godnosti'],
            upakovka=product['upakovka'],
            protein=product['protein'],
            fat=product['fat'],
            carbohydrate=product['carbohydrate'],
            calories=product['calories']
        )
        if photo_uri:
            try:
                await m.answer_photo(photo_uri,
                                     reply_markup=product_inline_kb(product_id=product['id']),
                                     caption=caption
                                     )
            except WrongFileIdentifier:
                photo_resp = await m.answer_photo(product['photo'],
                                                  reply_markup=product_inline_kb(product_id=product['id']),
                                                  caption=caption)
                await update_server_photo_uri(db,
                                              product_id=product['id'],
                                              file_id=photo_resp.photo[-1].file_id)
        elif product["photo_updated"] is True or not product["photo_uri"]:
            url = product['photo']
            parsed_url = urlparse(url)
            file_name: str = parsed_url.path.split("/")[-1]  # noqa
            try:
                with open("media/" + file_name, "rb") as file:
                    photo_resp = await m.answer_photo(
                        photo=file,
                        reply_markup=product_inline_kb(product_id=product['id']),
                        caption=caption
                    )
                    await update_server_photo_uri(db, product_id=product['id'],
                                                  file_id=photo_resp.photo[-1].file_id)
            except FileNotFoundError:
                photo_resp = await m.answer_photo(
                    photo=url,
                    reply_markup=product_inline_kb(product_id=product['id']),
                    caption=caption
                )
                await update_server_photo_uri(db, product_id=product['id'],
                                              file_id=photo_resp.photo[-1].file_id)
        await BuyState.get_cart.set()
    else:
        await m.answer(_("Iltimos ro'yxatdagi maxsulotni tanlang"))


async def get_cart(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("⬅️ Ortga"):  # noqa
        data = await state.get_data()
        products = await db.get_products(data.get("category"), user_lang)
        await m.answer(_("Muzqaymoq turini tanlang."),
                       reply_markup=generate_product_keyboard(products, user_lang))
        await BuyState.get_product.set()
        return
    elif m.text == _("📥 Savat"):
        await get_shopping_cart(m, db)


async def get_phone(m: Message, state: FSMContext, user_lang, db: Database):
    if m.content_type == types.ContentType.TEXT and m.text == _("⬅️ Ortga"):  # noqa
        await m.answer(_("Quyidagilardan birini tanlang", locale=user_lang),
                       reply_markup=main_menu_keyboard(user_lang))
        await MainMenuState.get_menu.set()
        return
    elif m.content_type == types.ContentType.TEXT: # noqa
        validator = validate_uzbek_phone_number(m.text)
        if validator:
            await state.update_data(contact=m.text)
        else:
            await m.answer(_("Iltimos, telefon raqamni ko'rsatilgan formatda yozing"))
            return
    else:
        # if m.contact.user_id != m.from_user.id:
        #     await m.answer(_("Iltimos ushbu telegram akauntga biriktirilgan telefon raqamini jo'nating"))
        #     return
        await state.update_data(contact=m.contact.phone_number)
    await m.answer(_("Toʻlov turini tanlang"), reply_markup=payment_method_btns())
    await BuyState.get_payment_method.set()


async def get_payment_method(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("⬅️ Ortga"):  # noqa
        await m.answer(
            _("Telefon raqamingizni quyidagi formatda "
              "yuboring yoki kiriting: +998 ** *** ** **\n"
              "Eslatma: Agar siz onlayn buyurtma uchun Click "
              "yoki Payme orqali toʻlashni rejalashtirmoqchi "
              "boʻlsangiz, tegishli xizmatda hisob qaydnomasi "
              "roʻyxatdan oʻtgan telefon raqamini koʻrsating."),
            reply_markup=get_contact_keyboard())
        await BuyState.get_phone.set()
        return
    else:
        # if m.contact.user_id != m.from_user.id:
        #     await m.answer(_("Iltimos ushbu telegram akauntga biriktirilgan telefon raqamini jo'nating"))
        #     return

        await state.update_data(payment_method=m.text)
        cart_items = await get_user_shopping_cart(m.from_user.id)
        if not cart_items:
            await m.answer(_("Savat bo'sh"))
        else:
            data = await state.get_data()
            cart_items_text, total_price = get_cart_items_text(cart_items)
            await m.answer(
                _(
                    "Sizning buyurtmangiz:\n"
                    "Manzil: {address}\n\n"
                    "{cart_items_text}\n"
                    "To'lov turi: {payment_method}\n\n"
                    "Mahsulotlar: {total_price} so'm\n"
                    "Yetkazib berish: {delivery} so'm\n"
                    "Jami: {cost} so'm"
                ).format(
                    address=data["address"],
                    payment_method=data["payment_method"],
                    cart_items_text=cart_items_text,
                    total_price=total_price,
                    delivery=db.DELIVERY_COST,
                    cost=int(db.DELIVERY_COST) + total_price
                ),
                reply_markup=approve_btns())
            await state.update_data(cost=int(db.DELIVERY_COST) + total_price)
        await BuyState.get_approve.set()


async def get_approve(m: Message, state: FSMContext, user_lang, db: Database, config: Config):
    if m.text == _("❌ Bekor qilish"):  # noqa
        await m.answer(_("Bo'limni tanlang.", locale=user_lang),
                       reply_markup=main_menu_keyboard(user_lang))
    else:
        data = await state.get_data()
        photo = (
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgWGCXrpS2g54YYm0eTzAHHFzY7Kj3ZXEcbg&usqp=CAU"
            if m.text == "Click" else "https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg")
        token = None
        price = None
        if data["payment_method"] == "Click":
            price = LabeledPrice(label="Click orqali to'lov", amount=data["cost"] * 100)
            token = config.misc.click
        elif data["payment_method"] == "Payme":
            price = LabeledPrice(label="Payme orqali to'lov", amount=data["cost"] * 100)
            token = config.misc.payme

        invoice_data = {
            "chat_id": m.from_user.id,
            "photo_url": photo,
            "currency": "uzs",
            "title": "Svitlogorie",
            "description": "Muzqaymoqlar haridi",
            "payload": "service-cart-payment",
            "provider_token": token,
            "prices": [price]
        }
        if invoice_data.get("provider_token"):
            await m.answer(_("Iltimos, quyidagi to'lovni amalga oshiring 👇"),
                           reply_markup=types.ReplyKeyboardRemove(selective=True))
            await m.bot.send_invoice(**invoice_data)
        else:
            cart_items = await get_user_shopping_cart(m.from_user.id)

            order_data = collect_data_for_request(
                data,
                cart_items,
                user_lang,
            )
            try:
                await db.create_order(order_data)
                cart_items_text, total_price = get_cart_items_text(cart_items)
                await send_to_group_order(m, config, data, cart_items_text, total_price, db)
                await m.answer("Siz bilan bog'lanishadi", reply_markup=main_menu_keyboard(user_lang))
            except Exception as _e:
                await m.answer(_("Serverdan xato o'tdi, birozdan so'ng xarakat qiling"),
                               reply_markup=main_menu_keyboard(user_lang))

            await clear_user_shopping_cart(m.from_user.id)

            await state.finish()
            await MainMenuState.get_menu.set()


async def pre_checkout_query(query: PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(query.id, ok=True)


async def success_payment(m: Message, config: Config, user_lang, state: FSMContext, db: Database):
    data = await state.get_data()
    cart_items = await get_user_shopping_cart(m.from_user.id)

    order_data = collect_data_for_request(
        data,
        cart_items,
        user_lang,
        m.successful_payment.provider_payment_charge_id
    )
    try:
        await db.create_order(order_data)
        cart_items_text, total_price = get_cart_items_text(cart_items)
        await send_to_group_order(m, config, data, cart_items_text, total_price, db)
        await m.answer(_("Sizning to'lovingiz muvaffaqiyatli o'tdi. Kuryer siz bilan bog'lanadi!"),
                       reply_markup=main_menu_keyboard(user_lang))
    except Exception as _e:
        await m.answer(_("Serverdan xato o'tdi, birozdan so'ng xarakat qiling"),
                       reply_markup=main_menu_keyboard(user_lang))
    await clear_user_shopping_cart(m.from_user.id)
    await state.finish()
    await MainMenuState.get_menu.set()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, state=MainMenuState.get_menu)
    dp.register_message_handler(menu, content_types=["text", "location"], state=BuyState.get_location)
    dp.register_message_handler(get_category, state=BuyState.get_category)
    dp.register_message_handler(get_product, state=BuyState.get_product)
    dp.register_message_handler(get_cart, state=BuyState.get_cart)
    dp.register_message_handler(get_phone, content_types=["text", "contact"], state=BuyState.get_phone)
    dp.register_message_handler(get_payment_method, state=BuyState.get_payment_method)
    dp.register_message_handler(get_approve, state=BuyState.get_approve)
    dp.register_pre_checkout_query_handler(pre_checkout_query, state="*")
    dp.register_message_handler(success_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT,
                                state="*")
