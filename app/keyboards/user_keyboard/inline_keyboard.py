from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_counter_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    quick = InlineKeyboardButton(text='Quick counter', callback_data='quick_counter')
    custom = InlineKeyboardButton(text='Custom counter', callback_data='custom_counter')

    markup.add(quick, custom)
    return markup
