from . import InlineKeyboardMarkup, InlineKeyboardButton

empty_keyboard = InlineKeyboardMarkup([]).to_json()

yes_no_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton('Да', callback_data='yes'),
    InlineKeyboardButton('Нет', callback_data='no'),
]]).to_json()
