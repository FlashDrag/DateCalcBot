import logging

from datetime import datetime, date, time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.user_keyboard.ikb_calendar import CalendarIkb, calendar_callback
from keyboards.user_keyboard.ikb_time import TimeIkb, time_callback

from states.user import CustomCounter

from utils.calculator import Calc

logger = logging.getLogger(__name__)


async def store_date(call: CallbackQuery,
                     state: FSMContext, selected_date: date, date_mark: str):
    '''
    Store start/end date to fsm storage appropriate to date_mark.
    Display time selection keyboard.
    '''
    async with state.proxy() as data:
        data[date_mark + '_date'] = selected_date

    await call.message.edit_text(f'Selected {date_mark} date')
    await call.message.answer(date.strftime(selected_date, "%d-%m-%Y"))
    await call.message.answer('Select time', reply_markup=await TimeIkb().display_time_ikb())
    await call.answer()


async def store_start_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call store_date func that stores the start date to fsm storage
    '''
    selected, date = await CalendarIkb().process_selection(call, callback_data)
    if selected:
        date_mark = 'start'
        await store_date(call, state, date, date_mark)
        await state.set_state(CustomCounter.set_start_time)


async def store_end_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call store_date func that stores the end date to fsm storage
    '''
    selected, date = await CalendarIkb().process_selection(call, callback_data)
    if selected:
        date_mark = 'end'
        await store_date(call, state, date, date_mark)
        await state.set_state(CustomCounter.set_end_time)


async def store_time(call: CallbackQuery, state: FSMContext, selected_time: time, time_mark: str):
    '''
    Store user selected start_time/end_time as a `time` object to fsm storage appropriate to the current time_mark.
    Display edited message with selected time to the user
    '''
    async with state.proxy() as data:
        # store time object to fsm storage
        data[time_mark + '_time'] = selected_time

    await call.message.edit_text(f'Selected {time_mark} time')
    await call.message.answer(time.strftime(selected_time, "%H:%M"))


async def submit_start_time(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    Provide the user to calendar and prompt select end date.
    '''
    selected, time = await TimeIkb().process_selection(call, callback_data)
    if selected:
        # call a func that stores selected time to fsm storage
        await store_time(call, state, time, 'start')

        await call.message.answer('Select end date', reply_markup=await CalendarIkb().display_calendar_ikb())
        await state.set_state(CustomCounter.set_end_date)
        await call.answer()


async def calculate(state: FSMContext):
    '''
    Gets stored data from fsm storage.
    If all related data is existed than passes start datetime and end datetime to Calc object.
    Calls getdifference() method on the Calc object with the selected time units list as an argument.
    :return: String of calculated data
    '''
    async with state.proxy() as data:
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        time_units = data.get('selected_units', None)

    if not all([start_date, end_date, start_time, end_time, time_units]):
        return 'Something went wrong. Try again!'

    # combines the start date and time and end date and time into datetime objects
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    try:
        calc = Calc(start_datetime, end_datetime)
        result_string = calc.get_difference(time_units)
    except Exception as e:
        logger.error(f'Calculation Error! {e}')
        return 'Something went wrong. Try again!'
    else:
        return result_string


async def submit_end_time(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    Call 'calculate' func that calculate the difference.
    Display result to the user
    '''
    selected, time = await TimeIkb().process_selection(call, callback_data)
    if selected:
        # call a func that stores selected time to fsm storage
        await store_time(call, state, time, 'end')

        result_string = await calculate(state)
        await call.message.answer(result_string)
        await call.answer()
        await state.finish()

        logger.info(f'\nUser: {call.from_user.full_name}, id: {call.from_user.id}\n{result_string}')


def register_time_select(dp: Dispatcher):
    dp.register_callback_query_handler(
        store_start_date, calendar_callback.filter(),
        state=CustomCounter.set_start_date
    )
    dp.register_callback_query_handler(
        submit_start_time, time_callback.filter(),
        state=CustomCounter.set_start_time
    )
    dp.register_callback_query_handler(
        store_end_date, calendar_callback.filter(),
        state=CustomCounter.set_end_date
    )
    dp.register_callback_query_handler(
        submit_end_time, time_callback.filter(),
        state=CustomCounter.set_end_time
    )
