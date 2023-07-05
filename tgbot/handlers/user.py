import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from tgbot.keyboards.reply import language_keyboards, main_menu_keyboard, languages
from tgbot.misc.states import UserRegisterState
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def user_start(message: Message, user_lang, **kwargs):
    logging.info(kwargs)
    logging.info('Start')
    await message.answer(_("Assalomu alaykum!\n"
                           "Botimizga xush kelibsiz!\n"
                           "Iltimos tilni tanlang"), reply_markup=language_keyboards())
    await UserRegisterState.get_lang.set()


async def get_user_lang(m: Message, state: FSMContext):
    if m.text not in languages:
        await m.answer(_("Iltimos ro'yxatdagi tugmalardan birini tanlang"))
    await state.update_data(lang=m.text)
    await m.answer(_("Iltimos telefon raqamingizni kiriting yoki tugmacha orqali yuboring"),
                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                       KeyboardButton(_("Kontaktni yuborish 📱"), request_contact=True)))
    await UserRegisterState.get_contact.set()


async def get_user_contact(m: Message, state: FSMContext):
    if m.contact.user_id != m.from_user.id:
        await m.answer(_("Iltimos ushbu telegram akauntga biriktirilgan telefon raqamini jo'nating"))
        return
    await state.update_data(contact=m.contact.phone_number)
    await m.answer(_("Iltimos manzilingizni kiriting yoki tugmacha orqali kiriting"),
                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                       KeyboardButton(_("Joylashuvni jo'natish🚩"), request_location=True)))
    await UserRegisterState.get_location.set()


async def get_user_location(m: Message, state: FSMContext, user_lang):
    await state.update_data(longitude=m.location.longitude,
                            latitude=m.location.latitude)
    await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_keyboard(user_lang))
    ...
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_user_lang, state=UserRegisterState.get_lang)
    dp.register_message_handler(get_user_contact, content_types='contact', state=UserRegisterState.get_contact)
    dp.register_message_handler(get_user_location, content_types='location', state=UserRegisterState.get_location)
