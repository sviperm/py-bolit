from . import InlineKeyboardMarkup, InlineKeyboardButton


def get_node_keyboard(node):
    buttons = [[
        InlineKeyboardButton(s, callback_data=f"{node['code']}${s}")
        for s in node['states']
    ]]
    return InlineKeyboardMarkup(buttons).to_json()
