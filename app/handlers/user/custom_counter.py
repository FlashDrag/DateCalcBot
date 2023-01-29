from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

from filters.user import TimeUnitsFilter
from filters.user import AllUnitsFilter
from filters.user import SubmitFilter
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
    '''
    Displays `time_units` selection menu and prompts the user select the `time_unit`
    '''
    await call.message.answer('Select the units of time to be calculated ⤵',
                              reply_markup=ikb_time_period())
    await call.answer()
    await state.set_state(CustomCounter.get_time_period)


async def process_custom_choice(call: CallbackQuery, state: FSMContext):
    '''
    Handles the callback query from the user selection.
    Stores/removes the user selected/deselected `time_units` to the state's storage as a lits of `selected_units`
    '''
    time_unit = call.data
    async with state.proxy() as data:
        units = data.setdefault('selected_units', [])
        if time_unit in units:
            data['selected_units'].remove(time_unit)
        else:
            data['selected_units'].append(time_unit)

        # update inline keyboard with selected/deselected time_units
        await call.message.edit_reply_markup(reply_markup=ikb_time_period(data['selected_units']))
    await call.answer()


async def process_all_units(call: CallbackQuery, state: FSMContext):
    # TODO check all time_units if the `Select all` inline button was clicked,
    # and after submit the state and provide the user to the calendar and set next state
    pass


async def process_submit(call: CallbackQuery, state: FSMContext):
    # TODO provide the user to the calendar and set next state

    print(await state.get_data())
    await state.finish()
    await call.answer()


def register_custom_counter(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.counter
        )
    dp.register_callback_query_handler(
        process_custom_choice, TimeUnitsFilter(), state=CustomCounter.get_time_period
    )
    dp.register_callback_query_handler(
        process_all_units, AllUnitsFilter(), state=CustomCounter.get_time_period
    )
    dp.register_callback_query_handler(
        process_submit, SubmitFilter(), state=CustomCounter.get_time_period
    )
