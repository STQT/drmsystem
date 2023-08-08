from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from tgbot.keyboards.reply import main_menu_keyboard
from tgbot.misc.states import MainMenuState


async def bot_echo(message: types.Message):
    # text = [
    #     "Эхо без состояния.",
    #     "Сообщение:",
    #     message.text
    # ]
    #
    # await message.answer('\n'.join(text))
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer("Выберите раздел.",
                             reply_markup=main_menu_keyboard())
        await MainMenuState.get_menu.set()
    else:
        ...


async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer("Выберите раздел",
                             reply_markup=main_menu_keyboard())
        await MainMenuState.get_menu.set()
    else:
        ...


# state_name = await state.get_state()
# text = [
#     f'Эхо в состоянии {hcode(state_name)}',
#     'Содержание сообщения:',
#     hcode(message.text)
# ]
# await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
