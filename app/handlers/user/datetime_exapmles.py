from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text


async def show_examples(message: Message):
    '''
    Displays the datetime example formates
    '''
    examples = "<code>1.06.2021\n1-1-2022\n25/12/22 04:00\n</code>" \
        "<code>1 Jan 23\n08 June 2023\n24 Aug 2024 20:00\n</code>" \
        "<i>It can be combined</i>"
    await message.answer(examples)


def register_datetime_examples(dp: Dispatcher):
    dp.register_message_handler(
        show_examples, Text(equals=['📋 Formates', 'Formates'], ignore_case=True), state='*')


# TODO Получаем язык юзера, и по locale показываем пример формата ввода
# Также этот формат ипользуем при выводе
