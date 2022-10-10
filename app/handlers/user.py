from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

# from app.services.repository import Repo
from states.user import UserMain, QuickCounter, CustomCounter

from keyboards.user_keyboard.inline_keyboard import ikb_menu, ikb_time_period

from calculator.example_datetime import show_datetime_formates
from calculator.quick_counter import quick_count


async def show_start_menu(message: Message, state: FSMContext):
    # await repo.add_user(message.from_user.id)
    await message.answer('Choose the date/time counter', reply_markup=ikb_menu())
    await state.set_state(UserMain.choose_counter)


async def cancel_action(message: Message, state: FSMContext):
    bot = message.bot
    await bot.delete_message(chat_id=message["chat"]['id'],
                             message_id=message.message_id-1)
    # await message.delete()
    await state.reset_state(with_data=False)
    await message.reply('<i>Canceled!</i>')
    await message.answer('Choose the date/time counter',
                         reply_markup=ikb_menu())
    await state.set_state(UserMain.choose_counter)


async def show_quick_counter_menu(call: CallbackQuery, state: FSMContext):
    bot = call.bot
    formates = show_datetime_formates()  # показать примеры ввода строки
    string = f'Input the START and END date/time in format:\n<b>day.month.year hour:minute</b>\n\n' \
        f'For example(<i>it can be combinate</i>):\n<code>{formates}</code>'
    await bot.send_message(call.from_user.id, string)
    await call.answer('The dash `-` must only be strictly between the dates.',
                      show_alert=True)
    await call.message.delete()
    await state.set_state(QuickCounter.get_string)


async def process_input_string(message: Message, state: FSMContext):
    result = quick_count(message.text)
    if result.startswith('Error:'):
        await message.reply(result)
        await message.answer('Try again and use correct format!')
        await state.set_state(QuickCounter.get_string)
    else:
        await message.reply(result)
        await state.finish()


async def show_custom_counter_menu(call: CallbackQuery, state: FSMContext):
    bot = call.bot
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Choose what you want to count',
                           reply_markup=ikb_time_period())

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
        show_quick_counter_menu, text='quick_counter', state=UserMain.choose_counter)
    dp.register_message_handler(
        process_input_string, state=QuickCounter.get_string)
    dp.register_callback_query_handler(
        show_custom_counter_menu, text='custom_counter', state=UserMain.choose_counter)
