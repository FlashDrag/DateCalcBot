from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start_process(m: Message):
    await m.answer('Hello, admin!')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_process, commands=['admin'], is_admin=True)
