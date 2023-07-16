from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


async def increase_count(callback_query: CallbackQuery):
    # Increase count logic here
    await callback_query.answer("Count increased")


async def decrease_count(callback_query: CallbackQuery):
    # Decrease count logic here
    await callback_query.answer("Count decreased")


async def show_count(callback_query: CallbackQuery):
    # Show count logic here
    await callback_query.answer(_("ta"))


async def add_to_cart(callback_query: CallbackQuery):
    # Add to cart logic here
    await callback_query.answer("Added to cart")


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(increase_count,
                                       lambda c: c.data.startswith == 'increase',
                                       state="*")
    dp.register_callback_query_handler(decrease_count,
                                       lambda c: c.data.startswith == 'decrease',
                                       state="*")
    dp.register_callback_query_handler(show_count,
                                       lambda c: c.data == 'count',
                                       state="*")
    dp.register_callback_query_handler(add_to_cart,
                                       lambda c: c.data == 'add_to_cart',
                                       state="*")
