from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from aiogram.utils.exceptions import ChatNotFound

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.keyboards.inline import approve_delivery_buy, organizations_keyboard
from tgbot.keyboards.reply import main_menu_keyboard
from tgbot.misc.states import UserRegisterState, MainMenuState
from tgbot.misc.i18n import i18ns
from tgbot.misc.utils import send_answer_organization

_ = i18ns.gettext


async def user_start(m: Message, db: Database, config: Config, state: FSMContext):
    if m.chat.type == types.ChatType.PRIVATE:
        # link = await create_invite_link(m.bot, config.tg_bot.channel_id, "HASHSUM")
        user = await db.get_user(user_id=m.from_user.id)
        if user[0] and user[0]['is_subscribed'] is True:
            await m.answer(_("Төменде берілген батырманы таңдаңыз"),
                           reply_markup=main_menu_keyboard())
            await MainMenuState.get_menu.set()
            return
        else:
            await db.create_or_update_user(user_id=m.from_user.id, fullname=m.from_user.full_name,
                                           username=m.from_user.username)
        await m.answer("Сәлеметсіз бе!\n"
                       "Shanyraq әуесқой дыбыстамалар жинағына арналған жазылымды осы "
                       "Shanyraq Bot арқылы сатып ала аласыз.\n"
                       "Жазылымдар жоспарын төменде көріп, өзіңізге қолайлысын таңдаңыз.")
        args = m.get_args()
        if args:
            org_slug = await send_answer_organization(m, db, args, config)
        else:
            organizations = await db.get_organizations_list()
            if organizations[0]:
                await m.answer("Қайсы дыбыстаушы студияны қолдап, жазылымды алғыңыз келеді?",
                               reply_markup=organizations_keyboard(organizations[0]))
            else:
                await m.answer("Жазбада ешқандай студия жоқ")
            return
        await UserRegisterState.send_tel.set()
        await state.update_data(org_slug=org_slug)
    else:
        ...


async def get_payment(m: Message, state: FSMContext, db: Database, config):
    if m.content_type != "photo":
        return await m.answer("Тек суреттер ғана қабылданады")
    data = await state.get_data()
    text = (f"Жаңа өтініш: {data['org_slug']}\n"
            f"Күндер саны: {data['days']}\n"
            f"Бағасы: {data['cost']}\n")
    try:
        file_id = m.photo[-1].file_id
        order_json = await db.create_order({
            "photo_uri": file_id,
            "cost": data["cost"],
            "user_id": m.from_user.id,
            "days": data["days"]
        })
        if order_json[1] in [200, 201]:
            await m.send_copy(data['group_id'])
            order_id = order_json[0]["id"]
            await m.bot.send_message(data['group_id'], text=text, reply_markup=approve_delivery_buy(order_id))
            await m.answer(_("Сіздің өтінішіңіз әкімшілерге тексеріске жіберілді. Күте тұрыңыз."),
                           reply_markup=main_menu_keyboard())
        else:
            await m.answer("Сізде әлдеқашан тексерістен өтпеген өтініштеріңіз бар. Өтініш, күте тұрыңыз.")
        await MainMenuState.get_menu.set()
    except ChatNotFound:
        await m.answer("Бұл студияның әкімші чаты табылмады. Басқа топтың әкімшісінен көмек сұраңыз")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_payment, state=UserRegisterState.get_payment, content_types=ContentTypes.ANY)
