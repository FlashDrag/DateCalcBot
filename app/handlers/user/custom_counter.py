from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text


# from app.services.repository import Repo
from states.user import UserMain, CustomCounter

from keyboards.user_keyboard.inline_keyboard import ikb_time_period

from calculator.calculator import DT, Calc


async def show_custom_counter_menu(call: CallbackQuery, state: FSMContext):
    await call.message.answer('What you need to get',
                              reply_markup=ikb_time_period())
    await call.answer()
    await state.set_state(CustomCounter.get_time_period)


def register_custom_counter(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.counter)
