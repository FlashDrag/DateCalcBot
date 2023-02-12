from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, CommandStart

# TODO DB
# from app.services.repository import Repo
from states.user import UserMain

from keyboards.user_keyboard.inline_keyboard import ikb_main_menu


async def show_start_menu(message: Message, state: FSMContext):
    '''
    Displays the start inline menu and prompts the user to select a date/time counter
    '''
    # TODO DB
    #  await repo.add_user(message.from_user.id)
    await message.answer('Select date/time counter ⤵', reply_markup=ikb_main_menu())
    await state.set_state(UserMain.counter)


async def show_info(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer(f'Welcome to DateTime Caclucator!\n'
                         'The Bot can calculate the difference between two dates '
                         'in different units of time and their combinations.\n'
                         '<b>Enter /start to display the menu!</b>')


async def cancel_action(message: Message, state: FSMContext):
    '''
    Resets state and displays the start inline menu
    '''
    await state.reset_state()
    await message.reply('<i>Canceled!</i>', reply_markup=ReplyKeyboardRemove())
    await message.answer('<b>Enter /start to display the menu!</b>')


def register_main(dp: Dispatcher):
    dp.register_message_handler(
        show_start_menu, CommandStart(), state=None)
    dp.register_message_handler(
        show_info, commands="info", state="*")
    dp.register_message_handler(
        cancel_action, commands="cancel", state="*")
    dp.register_message_handler(
        cancel_action, Text(equals=['cancel', 'stop'], ignore_case=True), state="*")
