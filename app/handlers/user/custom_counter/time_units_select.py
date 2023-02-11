from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters.user import TimeUnitsFilter
from filters.user import SubmitAllUnitsFilter
from filters.user import SubmitTimeUnitsFilter

from states.user import UserMain, CustomCounter

from utils.calendar import CalendarIkb
from keyboards.user_keyboard.inline_keyboard import ikb_time_units


async def show_custom_counter_menu(call: CallbackQuery, state: FSMContext):
    '''
    Displays `time_units` selection menu and prompts the user select the `time_unit`
    '''
    await call.message.answer('Select the units of time to be calculated ⤵',
                              reply_markup=ikb_time_units())
    await call.answer()
    await state.set_state(CustomCounter.get_time_units)


async def process_time_unit_select(call: CallbackQuery, state: FSMContext):
    '''
    Handles the callback query which is selected/deselected time_unit by the user.
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
        await call.message.edit_reply_markup(reply_markup=ikb_time_units(data['selected_units']))
    await call.answer()


async def process_all_units_select(call: CallbackQuery, state: FSMContext):
    '''
    Handles the callback query which is `Select all` from the user selection.
    Save all selected time units to the state's storage and update inline keyboard
    Submit the choice and provide the user to the calendar
    '''
    all_units = ["years", "months", "weeks", "days", "hours", "minutes"]

    async with state.proxy() as data:
        data['selected_units'] = all_units

    # display updated inline keyboard with all selected time units
    await call.message.edit_reply_markup(reply_markup=ikb_time_units(all_units))
    await call.message.answer('Select start date',
                              reply_markup=await CalendarIkb().display_calendar_ikb())
    await state.set_state(CustomCounter.set_start_date)
    await call.answer()


async def process_time_units_submit(call: CallbackQuery, state: FSMContext):
    '''
    Handles the callback query which is `Submit` from the user selection.
    Submit the choice and provide the user to the calendar
    '''
    async with state.proxy() as data:
        units = data.get('selected_units', [])
    if not units:
        await call.answer()
        return
    await call.message.answer('Select start date',
                              reply_markup=await CalendarIkb().display_calendar_ikb())
    await state.set_state(CustomCounter.set_start_date)
    await call.answer()


def register_time_units_select(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.counter
    )
    dp.register_callback_query_handler(
        process_time_unit_select, TimeUnitsFilter(), state=CustomCounter.get_time_units
    )
    dp.register_callback_query_handler(
        process_all_units_select, SubmitAllUnitsFilter(), state=CustomCounter.get_time_units
    )
    dp.register_callback_query_handler(
        process_time_units_submit, SubmitTimeUnitsFilter(), state=CustomCounter.get_time_units
    )
