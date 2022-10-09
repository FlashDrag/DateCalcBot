from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

# from app.services.repository import Repo
from states.user import UserMain, QuickCounter

from keyboards.user_keyboard.inline_keyboard import choose_counter_inline_keyboard

from calculator.example_datetime import show_datetime_formates
from calculator.quick_counter import quick_count


async def process_start_command(message: Message, state: FSMContext):
    # await repo.add_user(message.from_user.id)
    # bot = message.bot
    # bot.send_message(message.from_user.id, 'Hello!')
    await message.answer('Choose the date/time counter', reply_markup=choose_counter_inline_keyboard())
    # await state.set_state(UserMain.SOME_STATE)

# Quick counter / Custom counter


async def process_quick_counter(query: CallbackQuery, state: FSMContext):
    bot = query.bot
    formates = show_datetime_formates()  # показать примеры ввода строки
    string = f'Input the START and END date/time in format:\n<b>day.month.year hour:minute</b>\n\n' \
        f'For example(<i>it can be combinate</i>):\n<code>{formates}</code>'
    await bot.send_message(query.from_user.id, string)
    await query.answer('The <b>dash</b> `-` must only be strictly <i>between</i> the dates.', show_alert=True)
    await query.message.delete()
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
        process_start_command, commands=['start'], state=None)
    dp.register_callback_query_handler(
        process_quick_counter, text='quick_counter')
    dp.register_message_handler(
        process_input_string, state=QuickCounter.get_string)
