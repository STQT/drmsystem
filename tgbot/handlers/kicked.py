from aiogram import types, Dispatcher

from tgbot.db.queries import Database


async def stopped_users(my_chat_member: types.ChatMemberUpdated, db: Database):
    if my_chat_member.new_chat_member.status == "kicked":
        await db.update_user(my_chat_member.from_user.id, {"stopped": True})


def register_stopped_users(dp: Dispatcher):
    dp.register_my_chat_member_handler(stopped_users, state="*")
