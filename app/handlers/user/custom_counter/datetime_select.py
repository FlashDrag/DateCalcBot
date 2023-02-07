from datetime import datetime, date, time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from utils.calendar import InlineCalendar, calendar_callback

from filters.user import IncreaseTimeFilter, DecreaseTimeFilter, SubmitTimeFilter
from states.user import CustomCounter
from keyboards.user_keyboard.inline_keyboard import ikb_time_select

from utils.calculator import Calc

# TODO Refactor Time selection similar to calendar


async def store_date(call: CallbackQuery,
                     state: FSMContext, selected_date: date, date_mark: str):
    '''
    Store start/end date to fsm storage appropriate to date_mark.
    Display time selection keyboard.
    '''
    async with state.proxy() as data:
        data[date_mark + '_date'] = selected_date
        data['hour'] = 00
        data['minute'] = 00

    await call.message.edit_text(f'Selected {date_mark} date')
    await call.message.answer(date.strftime(selected_date, "%d-%m-%Y"))
    await call.message.answer('Select time', reply_markup=ikb_time_select())
    await call.answer()


async def store_start_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call store_date func that stores the start date to fsm storage
    '''
    selected, date = await InlineCalendar().process_selection(call, callback_data)
    if selected:
        date_mark = 'start'
        await store_date(call=call, state=state, selected_date=date, date_mark=date_mark)
        await state.set_state(CustomCounter.set_start_time)


async def store_end_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    '''
    Call store_date func that stores the end date to fsm storage
    '''
    selected, date = await InlineCalendar().process_selection(call, callback_data)
    if selected:
        date_mark = 'end'
        await store_date(call=call, state=state, selected_date=date, date_mark=date_mark)
        await state.set_state(CustomCounter.set_end_time)


async def increase_time(call: CallbackQuery, state: FSMContext):
    '''
    Increases the time by 1 hour or 5 minutes.
    Return new keyboard with changed time value
    '''
    time_unit = call.data
    async with state.proxy() as data:
        if time_unit.endswith('_hour'):
            # if the hour or minute is at the maximum value of 23 or 55 respectively - reset it to 0
            data['hour'] = (data['hour'] + 1) % 24
        else:
            data['minute'] = (data['minute'] + 5) % 60

        hour = data['hour']
        minute = data['minute']

    await call.message.edit_reply_markup(
        reply_markup=ikb_time_select(hour=hour, minute=minute)
    )
    await call.answer()


async def decrease_time(call: CallbackQuery, state: FSMContext):
    '''
    Decreases the time by 1 hour or 5 minutes.
    Return new keyboard with changed time value
    '''
    time_unit = call.data
    async with state.proxy() as data:
        # if the hour or minute is at the minimum value of zero, set it to 23 or 55 respectively
        if time_unit.endswith('_hour'):
            data['hour'] = (data['hour'] - 1) % 24
        else:
            data['minute'] = (data['minute'] - 5) % 60

        hour = data['hour']
        minute = data['minute']

    await call.message.edit_reply_markup(
        reply_markup=ikb_time_select(hour=hour, minute=minute)
    )
    await call.answer()


async def store_time(call: CallbackQuery, state: FSMContext, time_mark: str):
    '''
    Store user selected start_time/end_time as a `time` object to fsm storage appropriate to the current time_mark.
    Display edited message with selected time to the user
    '''
    async with state.proxy() as data:
        # create time object of datetime module
        selected_time: time = time(data['hour'], data['minute'])
        data[time_mark + '_time'] = selected_time  # store time object to fsm

    # remove time selection inline keyboard
    await call.message.delete_reply_markup()
    await call.message.edit_text(f'Selected {time_mark} time')
    await call.message.answer(time.strftime(selected_time, "%H:%M"))


async def submit_start_time(call: CallbackQuery, state: FSMContext):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    Provide the user to calendar and prompt select end date.
    '''
    # call a func that stores selected time to fsm storage
    await store_time(call, state, 'start')

    await call.message.answer('Select end date', reply_markup=await InlineCalendar().start_calendar())
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
        print(f'Calculation Error! {e}')
        return 'Something went wrong. Try again!'
    else:
        return result_string


async def submit_end_time(call: CallbackQuery, state: FSMContext):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    Call 'calculate' func that calculate the difference.
    Display result to the user
    '''
    # call a func that stores selected time to fsm storage
    await store_time(call, state, 'end')

    result_string = await calculate(state)
    await call.message.answer(result_string)
    await call.answer()
    await state.finish()


def register_time_select(dp: Dispatcher):
    dp.register_callback_query_handler(
        store_start_date, calendar_callback.filter(),
        state=CustomCounter.set_start_date
    )
    dp.register_callback_query_handler(
        increase_time, IncreaseTimeFilter(),
        state=[CustomCounter.set_start_time, CustomCounter.set_end_time]
    )
    dp.register_callback_query_handler(
        decrease_time, DecreaseTimeFilter(),
        state=[CustomCounter.set_start_time, CustomCounter.set_end_time]
    )
    dp.register_callback_query_handler(
        submit_start_time, SubmitTimeFilter(), state=CustomCounter.set_start_time
    )
    dp.register_callback_query_handler(
        store_end_date, calendar_callback.filter(),
        state=CustomCounter.set_end_date
    )
    dp.register_callback_query_handler(
        submit_end_time, SubmitTimeFilter(), state=CustomCounter.set_end_time
    )
