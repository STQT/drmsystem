import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.queries import Database
from tgbot.keyboards.reply import language_keyboards, main_menu_keyboard, settings_buttons, back_button
from tgbot.misc.states import SettingsState, MainMenuState
from tgbot.misc.i18n import i18ns
from tgbot.misc.utils import get_my_location_text

_ = i18ns.gettext


async def settings_menu(m: Message, user_lang, state: FSMContext, db: Database):
    if m.text == _("Tilni o'zgartirish"):
        await m.answer(_("Iltimos o'zgartirmoqchi bo'lgan tilingnizni tanlang"),
                       reply_markup=language_keyboards())
        await SettingsState.change_lang.set()
    elif m.text == _("🗺 Mening manzilim"):
        await get_my_location_text(m, user_lang, db)
        await SettingsState.change_address.set()
    elif m.text == _("⬅️ Ortga"):
        await state.finish()
        await m.answer(_("Bo'limni tanlang"), reply_markup=main_menu_keyboard(user_lang))
        await MainMenuState.get_menu.set()


async def change_language(m: Message, state: FSMContext, user_lang, db: Database):
    lang_dict = { # noqa
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
    await m.answer(_("Til muvaffaqiyatli o'zgartirildi", locale=user_lang))
    await state.finish()
    await m.answer("Sozlamalar", reply_markup=settings_buttons())
    await SettingsState.get_buttons.set()


async def change_address(m: Message, state: FSMContext, user_lang, db: Database):
    if m.text == _("Tozalash"):
        await db.delete_user_locations(m.from_user.id)
        await m.answer(_("Manzillar muvaffaqiyatli tozalandi", locale=user_lang))
        await state.finish()
    await m.answer(_("Sozlamalar"), reply_markup=settings_buttons())
    await SettingsState.get_buttons.set()


def register_settings(dp: Dispatcher):
    dp.register_message_handler(settings_menu, state=SettingsState.get_buttons)
    dp.register_message_handler(change_language, state=SettingsState.change_lang)
    dp.register_message_handler(change_address, state=SettingsState.change_address)
