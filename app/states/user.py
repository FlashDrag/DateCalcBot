from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMain(StatesGroup):
    counter = State()


class Counter(StatesGroup):
    start_datetime = State()
    end_datetime = State()


class CustomCounter(StatesGroup):
    get_time_units = State()
    set_start_date = State()
    set_start_time = State()
    set_end_date = State()
    set_end_time = State()
