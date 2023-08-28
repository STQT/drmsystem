from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.keyboards.inline import organizations_keyboard
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import UserRegisterState
from tgbot.misc.utils import send_answer_organization

_ = i18ns.gettext


async def process_callback(callback_query: CallbackQuery, db: Database, state: FSMContext):
    await callback_query.answer(text="Таңдалды")
    data = await state.get_data()
    org = await db.get_organization_obj(data['org_slug'])
    _id, days, cost = callback_query.data.split('_')
    await state.update_data(price_id=_id,
                            days=days,
                            cost=cost,
                            group_id=org[0]['group_id'])
    await callback_query.message.delete()
    kaspi_name = f"<b>{org[0]['kaspi_name']}</b>" if org[0]['kaspi_name'] else ""
    text = (f"Сіз {cost} теңгеге {days} күндік  жазылуды таңдадыңыз.\n"
            f"Жазылу үшін \n<b>{org[0]['kaspi']}</b> {kaspi_name}\nKaspi нөміріне көрсетілген соманы жіберіңіз. \n"
            f"Төлем жасалғаннан кейін, төлеміңізді растайтын чекты осы жерге жіберіңіз (скриншот).")
    await callback_query.message.answer(text)
    await UserRegisterState.get_payment.set()


async def pro_callback(callback_query: CallbackQuery, db: Database, config: Config):
    await callback_query.answer()
    _pro, answer, order_id = callback_query.data.split('_')
    user_mention = callback_query.from_user.mention
    new_text = callback_query.message.text + f"\nҚабылдаушы: {user_mention}"
    if answer == "yes":
        new_text += f"\nЖазба: <b>{order_id}</b>"
    else:
        new_text += "\n<b>Жазылым қабылданбады</b>"
    await callback_query.message.edit_text(new_text)

    edit_dict = {
        "yes": True,
        "no": False,
    }
    await db.update_order(order_id, {
        "is_approved": edit_dict[answer],
        "moderated_user": callback_query.from_user.full_name,
    })


async def upgrade_callback(callback_query: CallbackQuery, db: Database, config: Config):
    await callback_query.answer()
    organizations = await db.get_organizations_list()
    if organizations[0]:
        await callback_query.message.edit_text("Қайсы дыбыстаушы студияны қолдап, жазылымды алғыңыз келеді?"
                                               "(Жазылым ақшасы сол студияға түседі)",
                                               reply_markup=organizations_keyboard(organizations[0]))
    else:
        await callback_query.message.edit_text("Жазбада ешқандай студия жоқ")


async def get_organization_callback(callback_query: CallbackQuery, db: Database, config: Config, state: FSMContext):
    await callback_query.answer()
    _org, org_slug = callback_query.data.split('_')
    org_slug = await send_answer_organization(callback_query.message, db, org_slug, config, callback_query)
    await UserRegisterState.send_tel.set()
    await state.update_data(org_slug=org_slug)


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(pro_callback,
                                       lambda c: c.data.startswith('pro'),
                                       state="*")
    dp.register_callback_query_handler(upgrade_callback, lambda c: c.data == "upgrade",
                                       state="*")
    dp.register_callback_query_handler(get_organization_callback, lambda c: c.data.startswith('org_'),
                                       state="*")
    dp.register_callback_query_handler(process_callback,
                                       state="*")
