from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMain(StatesGroup):
    choose_counter = State()


class QuickCounter(StatesGroup):
    get_string = State()


class CustomCounter(StatesGroup):
    get_time_period = State()
