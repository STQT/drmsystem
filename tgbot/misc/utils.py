from aiogram import types

from tgbot.db.queries import Database
from tgbot.keyboards.reply import address_clear, back_button, locations_buttons
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def get_my_location_text(m: types.Message, user_lang, db: Database, remove_button=True):
    locations = await db.get_user_locations(m.from_user.id)
    if locations:
        loc_str = ""
        for num, location in enumerate(locations):
            loc_str += str(num + 1) + ". " + location['name'] + "\n"
        await m.answer(loc_str)
        await m.answer(_("O'z manzillaringizni tozalamoqchimisiz?"),
                       reply_markup=address_clear())
    else:
        await m.answer(_("Manzillar mavjud emas"), reply_markup=back_button(locale=user_lang))


async def get_my_location_for_select(m: types.Message, user_lang, db: Database):
    locations = await db.get_user_locations(m.from_user.id)
    if locations:
        await m.answer(_("Yetkazib berish manzilni tanlang"), reply_markup=locations_buttons(locations))
    else:
        await m.answer(_("Manzillar mavjud emas"), reply_markup=back_button(locale=user_lang))
