from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.misc.i18n import i18ns

languages = ("Uz", "Ru")

_ = i18ns.gettext


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Моя подписка")))
    keyboard.add(KeyboardButton(text=_("Мои заявки")))
    return keyboard
