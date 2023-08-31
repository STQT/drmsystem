from aiogram import Dispatcher
from aiogram.types import Message, ContentTypes, ChatType

from tgbot.db.queries import Database
from tgbot.keyboards.reply import admin_keyboards, cancel_keyboard
from tgbot.misc.states import BroadcastingState
from tgbot.misc.utils import broadcaster


async def admin_start(message: Message, state):
    if message.chat.type == ChatType.PRIVATE:
        await message.answer("Hello, admin!", reply_markup=admin_keyboards())
        await state.finish()
    else:
        ...


async def broadcasting(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await message.answer("Send me broadcasting content", reply_markup=cancel_keyboard())
        await BroadcastingState.get_content.set()
    else:
        ...


async def submit_broadcasting(message: Message, db: Database, state):
    if message.chat.type == ChatType.PRIVATE:
        if message.text == "❌ Cancel":
            pass
        else:
            await broadcaster(message, db)
        await message.answer("Hello, admin!", reply_markup=admin_keyboards())
        await state.finish()
    else:
        ...


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(submit_broadcasting,
                                content_types=ContentTypes.ANY,
                                state=BroadcastingState.get_content,
                                is_admin=True)
    dp.register_message_handler(broadcasting, state="*", is_admin=True)
