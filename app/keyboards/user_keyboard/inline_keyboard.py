from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    quick = InlineKeyboardButton(text='Quick counter', callback_data='quick_counter')
    custom = InlineKeyboardButton(text='Custom counter', callback_data='custom_counter')
    date_finder = InlineKeyboardButton(text='Date finder', callback_data='date_finder')

    markup.add(quick, custom, date_finder)
    return markup


def ikb_time_period():
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
