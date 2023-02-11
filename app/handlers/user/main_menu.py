from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
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


async def cancel_action(message: Message, state: FSMContext):
    '''
    Resets state and displays the start inline menu
    '''
    await state.reset_state(with_data=False)
    await message.reply('<i>Canceled!</i>')


def register_main(dp: Dispatcher):
    dp.register_message_handler(
        show_start_menu, CommandStart(), state=None)
    dp.register_message_handler(
        cancel_action, commands="cancel", state="*")
    dp.register_message_handler(
        cancel_action, Text(equals=['cancel', 'stop'], ignore_case=True), state="*")
