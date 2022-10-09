from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_counter_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    quick = InlineKeyboardButton(text='Quick counter', callback_data='quick_counter')
    custom = InlineKeyboardButton(text='Custom counter', callback_data='custom_counter')

    markup.add(quick, custom)
    return markup


def choose_time_period_inline_keyboard():
    markup = InlineKeyboardMarkup()
    years = InlineKeyboardButton(text='Years', callback_data='years')
    months = InlineKeyboardButton(text='Months', callback_data='months')
    weeks = InlineKeyboardButton(text='Weeks', callback_data='weeks')
    days = InlineKeyboardButton(text='Days', callback_data='days')
    hours = InlineKeyboardButton(text='Hours', callback_data='hours')
    minutes = InlineKeyboardButton(text='Minutes', callback_data='minutes')

    markup.row(years, months, weeks)
    markup.row(days, hours, minutes)
    return markup
