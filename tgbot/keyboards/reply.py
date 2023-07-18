from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.misc.i18n import i18ns

languages = ("Uz", "Ru", "En")

_ = i18ns.gettext


def language_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*[KeyboardButton(text=text) for text in languages])
    return keyboard


def get_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(_("📞 Mening raqamim"), request_contact=True))
    keyboard.add(KeyboardButton(_("⬅️ Ortga")))
    return keyboard


def main_menu_keyboard(locale):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Menyu", locale=locale)))
    keyboard.add(KeyboardButton(text=_("Izoh qoldirish", locale=locale)),
                 KeyboardButton(text=_("Sozlamalar", locale=locale)))
    return keyboard


def settings_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("🗺 Mening manzilim")),
                 KeyboardButton(text=_("Tilni o'zgartirish")))
    keyboard.add(KeyboardButton(text=_("⬅️ Ortga")))
    return keyboard


def address_clear():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Tozalash")))
    keyboard.add(KeyboardButton(text=_("⬅️ Ortga")))
    return keyboard


def back_button(locale):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("⬅️ Ortga", locale=locale)))
    return keyboard


def menu_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("🗺 Mening manzilim")))
    keyboard.add(KeyboardButton(text=_("📍 Manzil jo'natish"), request_location=True),
                 KeyboardButton(text=_("⬅️ Ortga")))
    return keyboard


def get_verification():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("✅ Ha")), KeyboardButton(text=_("❌ Yo'q")))
    keyboard.add(KeyboardButton(text=_("⬅️ Ortga")))
    return keyboard


def generate_category_keyboard(categories, user_lang):
    name_key = "name_" + user_lang
    # Create the ReplyKeyboardMarkup with two columns/rows
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        keyboard.add(KeyboardButton(category[name_key]))
    keyboard.add(KeyboardButton(_("⬅️ Ortga")), KeyboardButton("📥 Savat"))
    return keyboard


def generate_product_keyboard(products, user_lang):
    name_key = "name_" + user_lang
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    for product in products:
        button = KeyboardButton(product[name_key])
        keyboard.insert(button)
    keyboard.add(KeyboardButton(_("⬅️ Ortga")))

    return keyboard


def locations_buttons(locations):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for location in locations:
        keyboard.add(KeyboardButton(text=location['name']))
    keyboard.add(KeyboardButton(text=_("⬅️ Ortga")))
    return keyboard


def only_cart_and_back_btns():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(_("📥 Savat")))
    keyboard.add(KeyboardButton(_("⬅️ Ortga")))
    return keyboard


def payment_method_btns():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(_("Naqd pul")))
    keyboard.add(KeyboardButton(_("Click")))
    keyboard.add(KeyboardButton(_("Payme")))
    keyboard.add(KeyboardButton(_("⬅️ Ortga")))
    return keyboard


def approve_btns():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(_("✅ Tasdiqlash")))
    keyboard.add(KeyboardButton(_("❌ Bekor qilish")))
    return keyboard


def cancel_btn():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(_("❌ Bekor qilish")))
    return keyboard
