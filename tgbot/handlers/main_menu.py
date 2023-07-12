import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from tgbot.db.queries import Database
from tgbot.keyboards.reply import main_menu_keyboard, settings_buttons
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import MainMenuState, SettingsState

_ = i18ns.gettext


async def main_menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.text == _("Menyu", locale=user_lang):
        await m.answer("Menyu")
    elif m.text == _("Izoh qoldirish", locale=user_lang):
        await m.answer("Izoh qoldirish")
    elif m.text == _("Sozlamalar", locale=user_lang):
        await m.answer("Sozlamalar", reply_markup=settings_buttons())
        await SettingsState.get_buttons.set()
    else:
        await m.answer("Boshqa")


async def get_user_location(m: Message, state: FSMContext, user_lang):
    await state.update_data(longitude=m.location.longitude,
                            latitude=m.location.latitude)
    await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_keyboard(user_lang))
    data = await state.get_data()
    logging.info(data)
    await state.finish()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, state=MainMenuState.get_menu)
