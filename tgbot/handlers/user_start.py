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
        fullname=m.from_user.full_name,
        user_id=m.from_user.id,
        user_lang=m.from_user.language_code)
    user_lang = user.get("user_lang")
    if user:
        await m.answer(_("Bo'limni tanlang", locale=user_lang),
                       reply_markup=main_menu_keyboard(user_lang))
        await MainMenuState.get_menu.set()
        return
    await m.answer(_("Assalomu alaykum!\n"
                     "Botimizga xush kelibsiz!\n"
                     "Iltimos tilni tanlang"), reply_markup=language_keyboards())
    await UserRegisterState.get_lang.set()


async def get_user_lang(m: Message, state: FSMContext, db: Database):
    lang_dict = {
        "Uz": 'uz',
        "Ru": 'ru',
        "En": 'en',
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
    # await m.answer(_("Iltimos telefon raqamingizni kiriting yoki tugmacha orqali yuboring"),
    #                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
    #                    KeyboardButton(_("Kontaktni yuborish 📱"), request_contact=True)))
    # await UserRegisterState.get_contact.set()


# async def get_user_contact(m: Message, state: FSMContext, user_lang, db: Database):
#     if m.contact.user_id != m.from_user.id:
#         await m.answer(_("Iltimos ushbu telegram akauntga biriktirilgan telefon raqamini jo'nating"))
#         return
#     await state.update_data(contact=m.contact.phone_number)
#
#     data = await state.get_data()
#
#     await db.reg_user(
#         first_name=m.from_user.first_name,
#         user_id=m.from_user.id,
#         username=m.from_user.username,
#         contact=m.contact.phone_number,
#         user_lang=data['lang']
#     )
#     logging.info(data)
#     logging.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#     await state.finish()
#     await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_keyboard(user_lang))
#     await MainMenuState.get_menu.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_user_lang, state=UserRegisterState.get_lang)
    # dp.register_message_handler(get_user_contact, content_types='contact', state=UserRegisterState.get_contact)
