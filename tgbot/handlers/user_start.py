import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from tgbot.db.queries import Database
from tgbot.keyboards.reply import language_keyboards, main_menu_keyboard, languages
from tgbot.misc.states import UserRegisterState, MainMenuState
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def user_start(m: Message, db: Database):
    user = await db.get_user(
        username=m.from_user.username,
        fullname=m.from_user.full_name.replace("'", "´").replace('"', "”"),
        user_id=m.from_user.id,
        user_lang=m.from_user.language_code)

    if user:
        user_lang = user.get("user_lang")
        await m.answer(_("Bo'limni tanlang", locale=user_lang),
                       reply_markup=main_menu_keyboard(user_lang))
        await MainMenuState.get_menu.set()
        return
    await m.answer(_("Assalomu alaykum!\n"
                     "Botimizga xush kelibsiz!\n"
                     "Iltimos tilni tanlang", locale=m.from_user.language_code), reply_markup=language_keyboards())
    await UserRegisterState.get_lang.set()


async def get_user_lang(m: Message, state: FSMContext, db: Database):
    lang_dict = {
        "Uz": 'uz',
        "Ru": 'ru',
    }
    try:
        language = lang_dict[m.text]
    except KeyError:
        return await m.answer(_("Iltimos ro'yxatdagi tugmalardan birini tanlang"))
    await db.update_user(
        username=m.from_user.username,
        fullname=m.from_user.full_name,
        user_id=m.from_user.id,
        user_lang=language)
    await m.answer(_("Bo'limni tanlang", locale=language),
                   reply_markup=main_menu_keyboard(language))
    await MainMenuState.get_menu.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_user_lang, state=UserRegisterState.get_lang)
