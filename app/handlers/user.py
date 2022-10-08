from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# from app.services.repository import Repo
# from app.states.user import UserMain

from utils import calculator


async def process_start_command(message: Message, state: FSMContext):
    # await repo.add_user(message.from_user.id)
    # bot = message.bot
    # bot.send_message(message.from_user.id, 'Hello!')
    await message.answer('What do you need to count?')
    # await state.set_state(UserMain.SOME_STATE)


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
    dp.register_message_handler(process_start_command, commands=['start'], state='*')
