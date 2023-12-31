from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Менің жазылымым")))
    keyboard.add(KeyboardButton(text=_("Менің өтініштерім")))
    keyboard.add(KeyboardButton(text=_("Тіркелген арналар")))
    return keyboard


def admin_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("Broadcast messages")))
    return keyboard


def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=_("❌ Cancel")))
    return keyboard
