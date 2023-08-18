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
        if m.text == "Менің өтініштерім":
            applications = await db.get_user_orders(m.from_user.id)
            logging.info(applications[0])
            if not applications[0]:
                await m.answer("Сізде ешқандай өтініш жоқ")
            else:
                applications = applications[0]
                for app in applications:
                    date = app['created_at']
                    input_date_time = datetime.fromisoformat(date[:-6])
                    human_readable_date_time = input_date_time.strftime("%d-%m-%Y %H:%M")
                    status = "Мақұлданды" if app["is_approved"] else "Қабылданбады"
                    await m.answer_photo(
                        app["photo_uri"],
                        caption=f"Өтініш: {app['id']}\n"
                                f"{app['days']} күнге\n"
                                f"Сома: {app['cost']} теңге\n"
                                f"Жазылым: {status}\n"
                                f"Берілген уақыты: {human_readable_date_time}"
                    )
        elif m.text == "Менің жазылымым":
            subscribe = await db.get_user_subscribe(m.from_user.id)
            if subscribe[0]:
                created_at_datetime = datetime.strptime(subscribe[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                expiration_day_calculation = (f"{subscribe[0]['expiration_days']} "
                                              f"{'день' if subscribe[0]['days'] == 1 else 'дня'}")
                formatted_created_at = created_at_datetime.strftime("%d-%m-%Y")
                text_string = (
                    f"Жазылым мерзімі {expiration_day_calculation} күн\n"
                    f"Берілген уақыты: {formatted_created_at}\n"
                    f"Жазылым {subscribe[0]['days']} күнге ресімделді."
                )
                await m.answer(text_string,
                               reply_markup=upgrade_subscription_kb())
            else:
                await m.answer("Сізде белсенді жазылым жоқ")
        else:
            await m.answer("Төменде берілген батырманы таңдаңыз",
                           reply_markup=main_menu_keyboard())
            await MainMenuState.get_menu.set()
    else:
        ...

def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu, state=MainMenuState.get_menu)
