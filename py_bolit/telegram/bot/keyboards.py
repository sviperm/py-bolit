from . import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
               ReplyKeyboardMarkup)


def get_node_keyboard(node):
    buttons = [[
        InlineKeyboardButton(s, callback_data=f"{node['code']}${s}")
        for s in node['states']
    ]]
    return InlineKeyboardMarkup(buttons).to_json()


def get_reply_keyboard(names):
    buttons = [
        ['/result']
        [KeyboardButton(name)] for name in names
    ]
    return ReplyKeyboardMarkup(buttons).to_json()
