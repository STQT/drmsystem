from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    get_lang = State()
    get_name = State()
    get_contact = State()
    get_location = State()
