import logging

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentTypes, ReplyKeyboardRemove
from aiogram.utils.exceptions import ChatNotFound

from tgbot.config import Config
from tgbot.db.queries import Database
from tgbot.keyboards.inline import approve_delivery_buy
from tgbot.keyboards.reply import main_menu_keyboard, languages
from tgbot.misc.states import UserRegisterState, MainMenuState
from tgbot.misc.i18n import i18ns
from tgbot.misc.utils import send_answer_organization

_ = i18ns.gettext


async def user_start(m: Message, db: Database, config: Config, state: FSMContext):
    if m.chat.type == types.ChatType.PRIVATE:
        # link = await create_invite_link(m.bot, config.tg_bot.channel_id, "HASHSUM")
        user = await db.get_user(user_id=m.from_user.id)
        if user[0] and user[0]['is_subscribed'] is True:
            await m.answer(_("Выберите раздел"),
                           reply_markup=main_menu_keyboard())
            await MainMenuState.get_menu.set()
            return
        else:
            await db.create_or_update_user(user_id=m.from_user.id, fullname=m.from_user.full_name,
                                           username=m.from_user.username)
        await m.answer("Здравствуйте!\n"
                       "Добро пожаловать в бот!\n"
                       "Чтобы зайти в закрытый канал выберите тип подписки снизу")
        args = m.get_args()
        if args:
            org_slug = await send_answer_organization(m, db, args, config)
        else:
            org_slug = await send_answer_organization(m, db, "main", config)
        await UserRegisterState.send_tel.set()
        await state.update_data(org_slug=org_slug)
    else:
        ...


async def get_payment(m: Message, state: FSMContext, db: Database, config):
    if m.content_type != "photo":
        return await m.answer("Нужно только отправлять изображение")
    data = await state.get_data()
    text = (f"Новая заявка: {data['org_slug']}\n"
            f"Количество дней: {data['days']}\n"
            f"Сумма: {data['cost']}\n")
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
            await m.answer(_("Ваше сообщение отправлено для проверки в администраторы"),
                           reply_markup=main_menu_keyboard())
        else:
            await m.answer("Вы отправили уже много заявок, которые не рассмотрены, пожалуйста дождитесь подтверждения")
        await MainMenuState.get_menu.set()
    except ChatNotFound:
        await m.answer("Не найден чат модераторов данной студии. Обратитесь администраторам")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_payment, state=UserRegisterState.get_payment, content_types=ContentTypes.ANY)
