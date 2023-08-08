import logging
from datetime import datetime

from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.db.queries import Database
from tgbot.keyboards.inline import upgrade_subscription_kb
from tgbot.keyboards.reply import main_menu_keyboard
from tgbot.misc.states import MainMenuState


async def main_menu(m: Message, db: Database):
    if m.chat.type == types.ChatType.PRIVATE:
        if m.text == "Мои заявки":
            applications = await db.get_user_orders(m.from_user.id)
            logging.info(applications[0])
            if not applications[0]:
                await m.answer("У вас нет существующих заявок")
            else:
                applications = applications[0]
                for app in applications:
                    date = app['created_at']
                    input_date_time = datetime.fromisoformat(date[:-6])
                    human_readable_date_time = input_date_time.strftime("%d-%m-%Y %H:%M")
                    status = "Одобрено" if app["is_approved"] else "Отказано"
                    await m.answer_photo(
                        app["photo_uri"],
                        caption=f"Заявка: {app['id']}\n"
                                f"На: {app['days']} дней\n"
                                f"Сумма: {app['cost']} тенге\n"
                                f"Статус: {status}\n"
                                f"Создано: {human_readable_date_time}"
                    )
        elif m.text == "Моя подписка":
            subscribe = await db.get_user_subscribe(m.from_user.id)
            if subscribe[0]:
                created_at_datetime = datetime.strptime(subscribe[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                expiration_day_calculation = (f"{subscribe[0]['expiration_days']} "
                                              f"{'день' if subscribe[0]['days'] == 1 else 'дня'}")
                formatted_created_at = created_at_datetime.strftime("%d-%m-%Y")
                text_string = (
                    f"Срок действия подписки {expiration_day_calculation}\n"
                    f"Создано: {formatted_created_at}\n"
                    f"Подписка оформлена на {subscribe[0]['days']} {'день' if subscribe[0]['days'] == 1 else 'дня'}"
                )
                await m.answer(text_string,
                               reply_markup=upgrade_subscription_kb())
            else:
                await m.answer("Нет у вас активных подписок")
        else:
            await m.answer("Выберите раздел",
                           reply_markup=main_menu_keyboard())
            await MainMenuState.get_menu.set()
    else:
        ...

def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, state=MainMenuState.get_menu)
