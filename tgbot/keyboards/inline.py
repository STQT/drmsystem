from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.misc.i18n import i18ns
from tgbot.config import TOPICS

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


def approve_delivery_buy(order_id):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton(text="☑️ Мақұлдау",
                             callback_data=f'pro_yes_{order_id}'),
        InlineKeyboardButton(text=_("✖️ Қабылдамау"),
                             callback_data=f'pro_no_{order_id}'),
    )
    return inline_kb


def prices_keyboard(data):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in data:
        text = str(item['days']) + " күн " + str(item['cost']) + " теңге"
        button = InlineKeyboardButton(text=text,
                                      callback_data=str(item['id']) + "_" + str(item['days']) + "_" + str(item['cost']))
        inline_kb.insert(button)
    return inline_kb


def organizations_keyboard(org_list):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for item in org_list:
        text = item['name']
        button = InlineKeyboardButton(text=text,
                                      callback_data="org_" + item['slug'])
        inline_kb.insert(button)
    return inline_kb


def upgrade_subscription_kb():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton(text=_("📅 Жазылымды ұзарту"),
                             callback_data=f'upgrade'),
    )
    return inline_kb


def topics_keyboards():
    tg_url = "https://t.me/c/1530494054/"
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for name in TOPICS:
        inline_kb.add(
            InlineKeyboardButton(text=name,
                                 url=tg_url + TOPICS[name]),
        )
    return inline_kb
