from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, CommandStart

# from app.services.repository import Repo
from states.user import UserMain

from keyboards.user_keyboard.inline_keyboard import ikb_main_menu


async def show_start_menu(message: Message, state: FSMContext):
    '''
    Displays the start inline menu and prompts the user to select a date/time counter
    '''
    # await repo.add_user(message.from_user.id)
    await message.answer('Select a date/time counter ⤵', reply_markup=ikb_main_menu())
    # set state waiting for the user choise
    await state.set_state(UserMain.counter)


async def cancel_action(message: Message, state: FSMContext):
    '''
    Resets state and displays the start inline menu
    '''
    await state.reset_state(with_data=False)
    await message.reply('<i>Canceled!</i>')
    await message.answer('Select a date/time counter ⤵', reply_markup=ikb_main_menu())
    # set state waiting for the user choise
    await state.set_state(UserMain.counter)


'''
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


def register_main(dp: Dispatcher):
    dp.register_message_handler(
        show_start_menu, CommandStart(), state=None)
    dp.register_message_handler(
        cancel_action, commands="cancel", state="*")
    dp.register_message_handler(
        cancel_action, Text(equals=['cancel', 'stop'], ignore_case=True), state="*")
