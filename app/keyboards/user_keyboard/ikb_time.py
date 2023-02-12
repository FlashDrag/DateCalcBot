from datetime import datetime, time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
time_callback = CallbackData('time', 'act', 'hour', 'minute')


class TimeIkb:
    '''
    Time inline keyboard
    '''
    increase = '↑'
    increase_n = '↟'
    decrease = '↓'
    decrease_n = '↡'

    async def display_time_ikb(

        self,
        hour: int = datetime.utcnow().hour,
        minute: int = datetime.utcnow().minute
    ) -> InlineKeyboardMarkup:
        '''
        Display ikb with arrow selection
        '''
        markup = InlineKeyboardMarkup(row_width=2)
        # First row - increase buttons for n numbers
        markup.row()
        markup.insert(InlineKeyboardButton(
            text=self.increase_n,
            callback_data=time_callback.new("increase_n_hour", hour, minute)
        ))
        markup.insert(InlineKeyboardButton(
            text=self.increase_n,
            callback_data=time_callback.new("increase_n_minute", hour, minute)
        ))
        # Second row - increase buttons
        markup.row()
        markup.insert(InlineKeyboardButton(
            text=self.increase,
            callback_data=time_callback.new("increase_hour", hour, minute)
        ))
        markup.insert(InlineKeyboardButton(
            text=self.increase,
            callback_data=time_callback.new("increase_minute", hour, minute)
        ))
        # Third row - Hours, Minutes
        markup.insert(InlineKeyboardButton(
            text=hour,
            callback_data=time_callback.new("HOURS", hour, minute)
        ))
        markup.insert(InlineKeyboardButton(
            text=minute,
            callback_data=time_callback.new("MINUTES", hour, minute)
        ))
        # Fourht row - decrease buttons
        markup.row()
        markup.insert(InlineKeyboardButton(
            text=self.decrease,
            callback_data=time_callback.new("decrease_hour", hour, minute)
        ))
        markup.insert(InlineKeyboardButton(
            text=self.decrease,
            callback_data=time_callback.new("decrease_minute", hour, minute)
        ))
        # Fifth row - decrease buttons for n numbers
        markup.row()
        markup.insert(InlineKeyboardButton(
            text=self.decrease_n,
            callback_data=time_callback.new("decrease_n_hour", hour, minute)
        ))
        markup.insert(InlineKeyboardButton(
            text=self.decrease_n,
            callback_data=time_callback.new("decrease_n_minute", hour, minute)
        ))
        # Sixth row - submit
        markup.row()
        markup.insert(InlineKeyboardButton(
            text='Submit',
            callback_data=time_callback.new("submit_time", hour, minute)
        ))

        return markup

    async def _display_hours_ikb(
        self,
        hour: int = datetime.utcnow().hour,
        minute: int = datetime.utcnow().minute
    ) -> InlineKeyboardMarkup:
        '''
        Display hours 0-23 to select
        '''
        markup = InlineKeyboardMarkup(row_width=6)
        markup.row()
        for hour in range(0, 24):
            markup.insert(InlineKeyboardButton(
                hour,
                callback_data=time_callback.new('SET-HOUR', hour, minute)
            ))

        return markup

    async def _display_minutes_ikb(
        self,
        hour: int = datetime.utcnow().hour,
        minute: int = datetime.utcnow().minute
    ) -> InlineKeyboardMarkup:
        '''
        Display every 5th minutes from 0-55 to select
        '''
        markup = InlineKeyboardMarkup(row_width=6)
        markup.row()
        for minute in range(0, 56, 5):
            markup.insert(InlineKeyboardButton(
                minute,
                callback_data=time_callback.new('SET-MINUTE', hour, minute)
            ))

        return markup

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        '''
        Call class method appropriated to callback data and edit time inline keyboard.
        :return return_data: if time submitted by the user,
        tupple with True and datetime.time object will be returned
        '''
        return_data = (False, None)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        # user pressed a submit button, return time
        if data['act'] == "submit_time":
            await query.message.delete_reply_markup()   # removing inline keyboard
            # convert hour and minute to time using datetime.time
            return_data = True, time(
                int(data['hour']), int(data['minute']))

        if data['act'] == 'HOURS':
            await query.message.edit_reply_markup(
                await self._display_hours_ikb(int(data['hour']), int(data['minute']))
            )
        if data['act'] == 'MINUTES':
            await query.message.edit_reply_markup(
                await self._display_minutes_ikb(int(data['hour']), int(data['minute']))
            )

        if data['act'] == "SET-HOUR":
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), int(data['minute']))
            )
        if data['act'] == "SET-MINUTE":
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), int(data['minute']))
            )

        if data['act'] == "increase_hour":
            # if the hour or minute is at the maximum value of 23 or 55 respectively - reset it to 0
            next_hour = (int(data['hour']) + 1) % 24
            await query.message.edit_reply_markup(
                await self.display_time_ikb(next_hour, int(data['minute']))
            )
        if data['act'] == "increase_minute":
            next_minute = (int(data['minute']) + 1) % 60
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), next_minute)
            )
        if data['act'] == "decrease_hour":
            # if the hour or minute is at the minimum value of zero, set it to 23 or 55 respectively
            next_hour = (int(data['hour']) - 1) % 24
            await query.message.edit_reply_markup(
                await self.display_time_ikb(next_hour, int(data['minute']))
            )
        if data['act'] == "decrease_minute":
            next_minute = (int(data['minute']) - 1) % 60
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), next_minute)
            )

        if data['act'] == "increase_n_hour":
            # if the hour or minute is at the maximum value of 23 or 55 respectively - reset it to 0
            next_hour = (int(data['hour']) + 3) % 24
            await query.message.edit_reply_markup(
                await self.display_time_ikb(next_hour, int(data['minute']))
            )
        if data['act'] == "increase_n_minute":
            next_minute = (int(data['minute']) + 10) % 60
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), next_minute)
            )
        if data['act'] == "decrease_n_hour":
            # if the hour or minute is at the minimum value of zero, set it to 23 or 55 respectively
            next_hour = (int(data['hour']) - 3) % 24
            await query.message.edit_reply_markup(
                await self.display_time_ikb(next_hour, int(data['minute']))
            )
        if data['act'] == "decrease_n_minute":
            next_minute = (int(data['minute']) - 10) % 60
            await query.message.edit_reply_markup(
                await self.display_time_ikb(int(data['hour']), next_minute)
            )

        return return_data
