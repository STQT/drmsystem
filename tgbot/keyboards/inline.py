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
                             callback_data=f'addtocart_{str(product_count)}_{str(product_id)}'),
    )
    return inline_kb


def shopping_cart_kb(user_lang):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton(text=_("🛒 Maxsulot qo'shish", locale=user_lang),
                             callback_data='close'),
        InlineKeyboardButton(text=_('🚖 Buyurtma berish', locale=user_lang),
                             callback_data='buy'),
    )
    inline_kb.add(
        InlineKeyboardButton(text=_("🗑 Savatni tozalash", locale=user_lang),
                             callback_data=f'clean_trash'),
    )
    return inline_kb


def shopping_cart_clean_kb():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton(text="☑️ Xa",
                             callback_data='yes'),
        InlineKeyboardButton(text=_("✖️ Yo'q"),
                             callback_data='no'),
    )
    return inline_kb
