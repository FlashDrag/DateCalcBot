from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def formates_kb():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    request_location = False  # user.location is exist  # True/False from DB
    current_time = KeyboardButton(text='Current time', request_location=request_location)
    formates = KeyboardButton(text='Formates')

    markup.add(current_time, formates)
    return markup


def location_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    send_location = KeyboardButton(text=f'🗺 Определить автоматически', request_location=True)
    markup.add(send_location)
    return markup
