from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMain(StatesGroup):
    counter = State()


class Counter(StatesGroup):
    start_datetime = State()
    end_datetime = State()


class CustomCounter(StatesGroup):
    get_time_period = State()
