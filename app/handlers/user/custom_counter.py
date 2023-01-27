from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text


# from app.services.repository import Repo
from states.user import UserMain, CustomCounter

from keyboards.user_keyboard.inline_keyboard import ikb_time_period

from calculator.calculator import DT, Calc

'''
TODOs:
The selected/deselected time units (by the user using inline keyboard) will be added/removed in the state's storage
If the user pressed the `select all`:
all time units changes icons for selected and the select block will be automatically submitted
and user will be moved to the next state - date selecting

When the submit button will be pressed user will be prompted choose the dates in inline calendar
(firtly for test: the dates can be put manually)
The dates will be stored in the states storage

If the date choosen than specific function will be attemting to create Calc istance with passed datetime objects
Than the stored user selected time units will be looped and stored into the tupple
The existing units must be stored in specific order in the tupple: ("years", "months", "days", "hours", "minutes")
Than the tupple will be looped and for each unit will be called related Calc method which returns related number
'''


async def show_custom_counter_menu(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Select the units of time to be calculated ⤵',
                              reply_markup=ikb_time_period())
    await call.answer()
    await state.set_state(CustomCounter.get_time_period)


def register_custom_counter(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.counter)
