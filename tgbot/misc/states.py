from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    send_tel = State()
    get_payment = State()


class MainMenuState(StatesGroup):
    get_menu = State()
