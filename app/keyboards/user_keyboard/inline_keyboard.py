from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    quick = InlineKeyboardButton(text='📆 Quick counter', callback_data='quick_counter')
    custom = InlineKeyboardButton(text='⚙️ Custom counter', callback_data='custom_counter')
    date_finder = InlineKeyboardButton(text='🔎 Date finder', callback_data='date_finder')

    markup.add(quick, custom, date_finder)
    return markup


def ikb_time_period(selected_units=[]):
    '''
    Creates inline keyboard with checked/unchecked buttons that represent time_units
    :param list: all selected time units existing in the list will be checked
    :return: InlineKeyboardMarkup with checked/unchecked inline buttons
    '''
    markup = InlineKeyboardMarkup(row_width=3)
    units = ["years", "months", "weeks", "days", "hours", "minutes"]
    buttons = []

    checked = '🔘'
    unchecked = '⚪️'

    for unit in units:
        text = ' ' + unit.capitalize()
        # if time_unit in selected_units, it will be checked, otherwise - unchecked
        title = checked + text if unit in selected_units else unchecked + text
        buttons.append(InlineKeyboardButton(text=title, callback_data=unit))

    all_units = InlineKeyboardButton(text='✔️ Select all', callback_data='all_units')
    submit = InlineKeyboardButton(text='☑️ SUBMIT', callback_data='submit')

    markup.add(*buttons)
    markup.row(all_units)
    markup.row(submit)
    return markup
