from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.misc.i18n import i18ns

languages = ("Uz", "Ru", "En")

_ = i18ns.gettext


def language_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*[KeyboardButton(text=text) for text in languages])
    return keyboard


def main_menu_keyboard(locale):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Menyu", locale=locale)))
    keyboard.add(KeyboardButton(text=_("Izoh qoldirish", locale=locale)),
                 KeyboardButton(text=_("Sozlamalar", locale=locale)))
    return keyboard


def settings_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Mening manzilim")),
                 KeyboardButton(text=_("Tilni o'zgartirish")))
    keyboard.add(KeyboardButton(text=_("Orqaga")))
    return keyboard


def address_clear():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Tozalash")))
    keyboard.add(KeyboardButton(text=_("Orqaga")))
    return keyboard


def back_button(locale):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Orqaga", locale=locale)))
    return keyboard