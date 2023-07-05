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
