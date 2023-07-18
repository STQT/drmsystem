from aiogram import Dispatcher
from aiogram.types import Message, ContentType

from tgbot.config import Config
from tgbot.keyboards.reply import main_menu_keyboard
from tgbot.misc.states import ReviewState, MainMenuState
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def get_user_review(m: Message, config: Config, user_lang):
    text = _("Bo'limni tanlang")
    if m.text != _("❌ Bekor qilish"):
        text = _("Sizning xabaringiz mutasaddi hodimlarga jo'natildi.")
        await m.send_copy(config.tg_bot.group_id)

    await m.answer(text, reply_markup=main_menu_keyboard(user_lang))
    await MainMenuState.get_menu.set()


def register_review(dp: Dispatcher):
    dp.register_message_handler(get_user_review, state=ReviewState.get_review,
                                content_types=ContentType.ANY)
