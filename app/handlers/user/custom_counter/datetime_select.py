from datetime import date, time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Calendar

from filters.user import IncreaseTimeFilter, DecreaseTimeFilter, SubmitTimeFilter
from states.user import CustomCounter
from keyboards.user_keyboard.inline_keyboard import ikb_time_select


async def store_date(call: CallbackQuery, manager: DialogManager,
                     state: FSMContext, selected_date: date, date_mark: str):
    '''
    Store start/end date to fsm storage appropriate to date_mark.
    Display time selection keyboard.
    Close aiogram_dialog.
    '''
    async with state.proxy() as data:
        data[date_mark + '_date'] = selected_date
        data['hour'] = 00
        data['minute'] = 00

    await call.message.edit_text(f'Selected {date_mark} date')
    await call.message.answer(selected_date)
    await call.message.answer('Select time', reply_markup=ikb_time_select())

    # Close calendar widget and exit from dialog
    await manager.done()


async def store_start_date(call: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    '''
    Call store_date func that stores the start date to fsm storage
    '''
    date_mark = 'start'
    state = manager.data['state']
    await store_date(call=call, manager=manager, state=state, selected_date=selected_date, date_mark=date_mark)
    await state.set_state(CustomCounter.set_start_time)


async def store_end_date(call: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    '''
    Call store_date func that stores the end date to fsm storage
    '''
    date_mark = 'end'
    state = manager.data['state']
    await store_date(call=call, manager=manager, state=state, selected_date=selected_date, date_mark=date_mark)
    await state.set_state(CustomCounter.set_end_time)


async def increase_time(call: CallbackQuery, state: FSMContext):
    time_unit = call.data
    async with state.proxy() as data:
        if time_unit.endswith('_hour'):
            if data['hour'] == 23:
                data['hour'] = 00
            else:
                data['hour'] += 1
        else:
            if data['minute'] == 55:
                data['minute'] = 00
            else:
                data['minute'] += 5

        hour = data['hour']
        minute = data['minute']

    await call.message.edit_reply_markup(
        reply_markup=ikb_time_select(hour=hour, minute=minute)
    )
    await call.answer()


async def decrease_time(call: CallbackQuery, state: FSMContext):
    time_unit = call.data
    async with state.proxy() as data:
        if time_unit.endswith('_hour'):
            if data['hour'] == 0:
                data['hour'] = 23
            else:
                data['hour'] -= 1
        else:
            if data['minute'] == 0:
                data['minute'] = 55
            else:
                data['minute'] -= 5

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
    await call.message.answer(selected_time)
    await call.answer()


async def submit_start_time(call: CallbackQuery, dialog_manager: DialogManager):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    Start aiogram_dialog with Calendar widget.
    '''
    state = dialog_manager.data['state']  # get a state from dialog_manager data object
    # call a func that stores selected time to fsm storage
    await store_time(call, state, 'start')

    # back to dialog, display calendar
    await dialog_manager.start(CustomCounter.set_end_date, mode=StartMode.RESET_STACK)


async def submit_end_time(call: CallbackQuery, dialog_manager: DialogManager):
    '''
    Call `store_time` func that stores selected time as a `time` object to fsm storage.
    '''
    state = dialog_manager.data['state']  # get a state from dialog_manager data object
    # call a func that stores selected time to fsm storage
    await store_time(call, state, 'end')

    print(await state.get_data())
    await state.finish()


"""DIALOG"""
date_select_dialog = Dialog(
    Window(
        Const('Select start date'),
        Calendar(id='calendar', on_click=store_start_date),
        state=CustomCounter.set_start_date
    ),
    Window(
        Const('Select end date'),
        Calendar(id='calendar', on_click=store_end_date),
        state=CustomCounter.set_end_date
    )
)


def register_time_select(dp: Dispatcher):
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
        submit_end_time, SubmitTimeFilter(), state=CustomCounter.set_end_time
    )
