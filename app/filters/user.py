from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class TimeUnitsFilter(BoundFilter):
    """
    Check callback_query updates.
    Return True if the callback_query in `time_units` tuple
    """
    time_units = ("years", "months", "weeks", "days", "hours", "minutes")

    async def check(self, callback_query: CallbackQuery):
        if callback_query and callback_query.data in self.time_units:
            return True
        return False


class AllUnitsFilter(BoundFilter):
    """
    Check callback_query updates.
    Return True if the callback_query is `all_units`
    """
    async def check(self, callback_query: CallbackQuery):
        if callback_query and callback_query.data == 'all_units':
            return True
        return False


class SubmitFilter(BoundFilter):
    """
    Check callback_query updates.
    Return True if the callback_query is `submit`
    """
    async def check(self, callback_query: CallbackQuery):
        if callback_query and callback_query.data == 'submit':
            return True
        return False
