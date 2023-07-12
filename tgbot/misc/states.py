from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    get_lang = State()
    get_name = State()
    get_contact = State()
    get_location = State()


class MainMenuState(StatesGroup):
    get_menu = State()


class SettingsState(StatesGroup):
    get_buttons = State()
    change_lang = State()
    get_lang = State()
    change_address = State()