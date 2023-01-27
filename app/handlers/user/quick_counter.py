from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove


# from app.services.repository import Repo
from states.user import UserMain, Counter

from keyboards.user_keyboard.default_keyboard import formates_kb
from keyboards.user_keyboard.inline_keyboard import ikb_main_menu

from calculator.calculator import DT, Calc


async def request_start_datetime(call: CallbackQuery, state: FSMContext):
    """
    Sends a message to the user asking for the start date and time
    and provides a keyboard to show datetime examples.
    """
    string = f'Put the START date/time in format:\n' \
        f'<code><b>DD.MM.YYYY HH:MM</b></code>'
    await call.message.answer(string, reply_markup=formates_kb())
    await call.answer('To show examples, text /formates')
    await state.set_state(Counter.start_datetime)


async def process_start_string(message: Message, state: FSMContext):
    '''
    Processes the start date/time string entered by the user,
    creates a DT instance and converts the string to datetime format.
    - If the string is in an incorrect format, the user is notified and prompted to try again.
    - If the string is in the correct format,
      the DT instance is saved to the state's storage and
      the user is prompted to provide the end date/time.

    :param message: The user-provided start date/time string in tg message format
    :param state: The state object used to store and retrieve data during the conversation
    '''
    try:
        # create DT instance and convert str to datetime format
        st_datetime = DT(message.text)
    except Exception as e:
        print(f'Incorrect data format of the start date/time string\n'
              f'{type(e).__name__}: {e}')
        await message.reply('Incorrect data format. Try again!')
        await state.set_state(Counter.start_datetime)
    else:
        async with state.proxy() as dt:
            dt['st_datetime'] = st_datetime  # save DT instance to storage
        string = f'Put the END date/time in format:\n' \
            f'<code><b>DD.MM.YYYY HH:MM</b></code>'
        # provides a keyboard to show datetime examples
        await message.answer(string, reply_markup=formates_kb())
        # set state waiting for end_datetime
        await state.set_state(Counter.end_datetime)


async def process_end_string(message: Message, state: FSMContext):
    '''
    Handles the end date/time string entered by the user.
    Process the string creating a DT instance and converts the string to datetime format.
    - If it fails to create the instance,
      it raises an exception and sends an error message to the user and sets the state back to Counter.end_datetime.
    - If successful:
        - it saves the `end_datetime` instance to the state's storage.
        - retrieves the start and end datetimes from the storage and
          converts them to strings.
        - attempts to create `Calc` instance with the start and end datetime objects
          which are receiving using DT class method `get_datetime()`
            - if it fails, it raises an exception and sends an error message to the user and finishes the state.
            - if successful, it retrieves the result of the calculation in string format and sends it to the user
    '''
    try:
        # create DT instance and convert str to datetime format
        end_datetime = DT(message.text)
    except Exception as e:
        print(f'Incorrect data format of the end date/time string!\n'
              f'{type(e).__name__}: {e}')
        await message.reply('Incorrect data format. Try again!')
        await state.set_state(Counter.end_datetime)
    else:
        async with state.proxy() as dt:
            dt['end_datetime'] = end_datetime  # save DT instance to storage

            # convert datetime to human format string
            start = str(dt['st_datetime'])
            end = str(dt['end_datetime'])
        try:
            # Get DT instances from storage and get datetime attribute
            # which is datetime object using DT.get_datetime() method.
            # Create Calc instance with datetime attributes
            calc = Calc(dt['st_datetime'].get_datetime(),
                        dt['end_datetime'].get_datetime())
        except Exception as e:
            print(
                f'Error of creating `Calc` instance!\n {type(e).__name__}: {e}')
            await message.answer('Something Went Wrong, Please Try Again', reply_markup=ikb_main_menu())
            await state.finish()
        else:
            # get quick result from Calc instance in string format with time period data
            result = str(calc)
            await message.answer(f'<i>{start} - {end}</i>:\n{result}', reply_markup=ReplyKeyboardRemove())
            await state.finish()


def register_quick_counter(dp: Dispatcher):

    dp.register_callback_query_handler(
        request_start_datetime, text='quick_counter', state=UserMain.counter)
    dp.register_message_handler(
        process_start_string, state=Counter.start_datetime)
    dp.register_message_handler(
        process_end_string, state=Counter.end_datetime)
