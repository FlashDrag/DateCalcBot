from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove


# from app.services.repository import Repo
from states.user import UserMain, Counter, CustomCounter

from keyboards.user_keyboard.inline_keyboard import ikb_main_menu, ikb_time_period
from keyboards.user_keyboard.default_keyboard import formates_kb

from calculator.example_datetime import show_datetime_formates
from calculator.calculator import DT, Calc


async def show_start_menu(message: Message, state: FSMContext):
    # await repo.add_user(message.from_user.id)
    await message.answer('Choose the date/time counter', reply_markup=ikb_main_menu())
    await state.set_state(UserMain.counter)


async def cancel_action(message: Message, state: FSMContext):
    # bot = message.bot
    # await bot.delete_message(chat_id=message["chat"]['id'],
    #                          message_id=message.message_id-1)
    # await message.delete()
    await state.reset_state(with_data=False)
    await message.reply('<i>Canceled!</i>')
    await message.answer('Choose the date/time counter', reply_markup=ikb_main_menu())
    await state.set_state(UserMain.counter)


# TODO: Create module for quick_counter handlers and separate them (to leave clean main module)
async def request_start_datetime(call: CallbackQuery, state: FSMContext):
    bot = call.bot
    # formates = show_datetime_formates()  # показать примеры ввода строки
    string = f'Put the START date/time in format:\n' \
        f'<code><b>DD.MM.YYYY HH:MM</b></code>'
    await bot.send_message(call.from_user.id, string, reply_markup=formates_kb())
    await call.answer('To show examples, text /formates')
    await call.message.delete()
    await state.set_state(Counter.start_datetime)


async def process_start_string(message: Message, state: FSMContext):
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
        await message.answer(string, reply_markup=formates_kb())
        await state.set_state(Counter.end_datetime)


async def process_end_string(message: Message, state: FSMContext):
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
            # get DT instance from storage and get datetime attribute using DT.get_datetime() method
            # create Calc instance with datetime attributes
            calc = Calc(dt['st_datetime'].get_datetime(),
                        dt['end_datetime'].get_datetime())
        except Exception as e:
            print(
                f'Error of creating `Calc` instance!\n {type(e).__name__}: {e}')
            await message.answer('Something Went Wrong, Please Try Again')
            await state.finish()
        else:
            # get quick result from Calc instance in string format with time period data
            result = str(calc)
            await message.answer(f'<i>Between</i>\n{start} and {end}:\n{result}', reply_markup=ReplyKeyboardRemove())
            await state.finish()


async def show_custom_counter_menu(call: CallbackQuery, state: FSMContext):
    bot = call.bot
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'What you need to get',
                           reply_markup=ikb_time_period)

    await call.answer()
    await state.set_state(CustomCounter.get_time_period)


'''
# выберите что нужно посчитать (user выбирает нажатием инлайн кнопок, выбор добавляеться в список user_choice)
user_choice = 'weeks-minutes'

# От которой даты и/или времени считаем? `Текущее` или `ввдите дату и время(опционально)5-07-2021 14:00
# Задаем в переменную либо дату и время котороую ввел юзер, либо текущее
choice_start_date_time = 'Текущее'
try:
    # валидируем строки и получаем datetime
    start_date = calculator.get_date_time(choice_start_date_time)
except Exception as e:
    print(e, 'некорректный формат')
    print(type(e).__name__, 'get_date_time')
    # do something
# else:
    # print(calculate(user_choice, start_date, end_date))


# _ДО_ которой даты и времени считаем? `Текущая` | `Ввести дату и время`
# Введите конечную дату и время `число-месяц-год`, например 5-07-2023 15.00
choice_end_date_time = '5-07-2023 15:00'
try:
    # валидируем строки и получаем datetime
    end_date = calculator.get_date_time(choice_end_date_time)
except Exception as e:
    print(e, 'некорректный формат')
    print(type(e).__name__, 'get_date_time')


print(calculator.calculate(user_choice, start_date, end_date))
'''


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        show_start_menu, commands=['start'], state=None)
    dp.register_message_handler(
        cancel_action, commands="cancel", state="*")
    dp.register_message_handler(
        cancel_action, Text(equals=['cancel', 'stop'], ignore_case=True), state="*")

    dp.register_callback_query_handler(
        request_start_datetime, text='quick_counter', state=UserMain.counter)
    dp.register_message_handler(
        process_start_string, content_types=['text'], state=Counter.start_datetime)
    dp.register_message_handler(
        process_end_string, content_types=['text'], state=Counter.end_datetime)

    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.counter)
