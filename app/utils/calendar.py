import calendar
from datetime import datetime, timedelta, date

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')

'''
Inline calendar based on noXplode's 'aiogram_calendar'
source: https://github.com/noXplode/aiogram_calendar
noXplode's 'SimpleCalendar' and 'DialogCalendar' were merged in single `InlineCalendar` class
'''


class CalendarIkb:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ignore_callback = calendar_callback.new(
        "IGNORE", 0, 0, 0)  # for buttons with no answer

    async def display_calendar_ikb(
        self,
        year: int = datetime.now().year,
        month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        inline_kb = InlineKeyboardMarkup(row_width=7)
        # First row - Month and Year
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<<",
            callback_data=calendar_callback.new("PREV-YEAR", year, month, 1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=calendar_callback.new('YEARS', year, month, 1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            ">>",
            callback_data=calendar_callback.new("NEXT-YEAR", year, month, 1)
        ))
        # Second row - Week Days
        inline_kb.row()
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            inline_kb.insert(InlineKeyboardButton(
                day, callback_data=self.ignore_callback))

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if (day == 0):
                    inline_kb.insert(InlineKeyboardButton(
                        " ", callback_data=self.ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=calendar_callback.new("DAY", year, month, day)
                ))

        # Last row - Buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<", callback_data=calendar_callback.new("PREV-MONTH", year, month, day)
        ))
        inline_kb.insert(InlineKeyboardButton(
            calendar.month_name[month], callback_data=calendar_callback.new("MONTHS", year, month, day)))
        inline_kb.insert(InlineKeyboardButton(
            ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, day)
        ))

        return inline_kb

    async def _display_years_ikb(self, year: int = datetime.now().year) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        inline_kb.row()
        for value in range(year - 7, year + 8):
            inline_kb.insert(InlineKeyboardButton(
                value,
                callback_data=calendar_callback.new('SET-YEAR', value, 1, 1)
            ))
        # nav buttons
        inline_kb.insert(InlineKeyboardButton(
            '<<',
            callback_data=calendar_callback.new('PREV-YEARS', year, 1, 1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            '>>',
            callback_data=calendar_callback.new('NEXT-YEARS', year, 1, 1)
        ))

        return inline_kb

    async def _display_months_ikb(
        self, year: int = datetime.now().year, month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=6)
        # first row with year button
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            " ",
            callback_data=self.ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=calendar_callback.new('YEARS', year, month, 1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            " ",
            callback_data=self.ignore_callback
        ))
        # three rows with 4 months buttons
        inline_kb.row()
        for month in self.months[0:4]:
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=calendar_callback.new(
                    "SET-MONTH", year, self.months.index(month) + 1, -1)
            ))
        inline_kb.row()
        for month in self.months[4:8]:
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=calendar_callback.new(
                    "SET-MONTH", year, self.months.index(month) + 1, -1)
            ))
        inline_kb.row()
        for month in self.months[8:12]:
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=calendar_callback.new(
                    "SET-MONTH", year, self.months.index(month) + 1, -1)
            ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        # user picked a day button, return date
        if data['act'] == "DAY":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, date(
                int(data['year']), int(data['month']), int(data['day']))
        # user navigates to previous year, editing message with new calendar
        if data['act'] == "PREV-YEAR":
            prev_date = datetime(int(data['year']) - 1, int(data['month']), 1)
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(prev_date.year),
                                                                                  int(prev_date.month)))
        # user navigates to next year, editing message with new calendar
        if data['act'] == "NEXT-YEAR":
            next_date = datetime(int(data['year']) + 1, int(data['month']), 1)
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(next_date.year),
                                                                                  int(next_date.month)))
        # user navigates to previous month, editing message with new calendar
        if data['act'] == "PREV-MONTH":
            prev_date = datetime(int(data['year']), int(data['month']), 1) - timedelta(days=1)
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(prev_date.year),
                                                                                  int(prev_date.month)))
        # user navigates to next month, editing message with new calendar
        if data['act'] == "NEXT-MONTH":
            next_date = datetime(int(data['year']), int(data['month']), 1) + timedelta(days=31)
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(next_date.year),
                                                                                  int(next_date.month)))
        if data['act'] == 'MONTHS':
            await query.message.edit_reply_markup(await self._display_months_ikb(int(data['year']),
                                                                                 int(data['month'])))
        if data['act'] == "SET-MONTH":
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(data['year']),
                                                                                  int(data['month'])))
        if data['act'] == "SET-YEAR":
            await query.message.edit_reply_markup(await self.display_calendar_ikb(int(data['year'])))
        if data['act'] == 'YEARS':
            await query.message.edit_reply_markup(await self._display_years_ikb(int(data['year'])))
        if data['act'] == 'PREV-YEARS':
            new_year = int(data['year']) - 15
            await query.message.edit_reply_markup(await self._display_years_ikb(new_year))
        if data['act'] == 'NEXT-YEARS':
            new_year = int(data['year']) + 15
            await query.message.edit_reply_markup(await self._display_years_ikb(new_year))

        return return_data
