from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


def product_inline_kb(product_id, product_count=1):
    inline_kb = InlineKeyboardMarkup(row_width=3)
    inline_kb.add(
        InlineKeyboardButton(text='-',
                             callback_data=f'decrease_{str(product_count)}_{str(product_id)}'),
        InlineKeyboardButton(text=f'{product_count}', callback_data='count'),
        InlineKeyboardButton(text='+',
                             callback_data=f'increase_{str(product_count)}_{str(product_id)}'),
    )
    inline_kb.add(
        InlineKeyboardButton(text=_("📥 Savatga qo'shish"),
                             callback_data=f'add_to_cart_{str(product_count)}_{str(product_id)}'),
    )
    return inline_kb
