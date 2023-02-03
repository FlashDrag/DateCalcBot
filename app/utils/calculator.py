from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime


class DT:
    '''
    This class is used to parse a user-provided date/time string into a datetime object.
    Creating new instance takes user provided date/time string and
    sets the datetime attribute by calling the set_datetime method
    '''
    def __init__(self, user_datetime_string: str):
        self.set_datetime(user_datetime_string)

    def get_datetime(self):
        '''
        Returns a parsed datetime value as datetime object
        '''
        return self.__datetime

    def set_datetime(self, value):
        '''
        Attempts to intelligently the user-provided date/time string into a datetime object
        and sets the `__datetime` attribute
        :param value: user-provided date/time string
        '''
        # dayfirst=True gives precedence to the DD-MM-YYYY format instead of MM-DD-YYYY
        # in cases where the date format is ambiguous
        dt = parse(value, dayfirst=True)
        self.__datetime = dt

    def __str__(self) -> str:
        '''
        Returns the string representation of the datetime object in specific format
        '''
        res = datetime.strftime(self.get_datetime(), '%d %b %y %H:%M')  # set output string in format: DD-MM-YY H:M
        print(res)
        return res


class Calc:
    '''
    Calculates the difference between two dates in different units of time and their combinations.
    :param start_date: The start date as a datetime object
    :param end_date: The end date as a datetime object
    '''

    UNITS = ("years", "months", "weeks", "days", "hours", "minutes")

    def __init__(self, start_date: datetime, end_date: datetime):
        if not isinstance(start_date, datetime):
            raise TypeError('start_date must be a datetime object')
        if not isinstance(end_date, datetime):
            raise TypeError('end_date must be a datetime object')

        self.start_date, self.end_date = min(start_date, end_date), max(start_date, end_date)

        self._r_delta = self.get_r_delta()
        self._delta = self.get_delta()

        self._years = None
        self._months = None
        self._weeks = None
        self._days = None
        self._hours = None
        self._minutes = None

    def get_difference(self, time_units: list) -> str:
        '''
        Sorts the selected time_units based on the position of its elements in the UNITS tuple.
        In right order, calls class methods appropriated to existed time_units and return values of time.
        :param time_units: user selected units of time
        :return: String-result with time unit names and its values
        '''

        sorted_time_units = sorted(time_units, key=self.UNITS.index)
        result_lst = []

        for unit_name in sorted_time_units:
            time_unit_num = getattr(self, unit_name)()
            if not time_unit_num:
                continue
            result_lst.append(f'{unit_name.capitalize()}: {time_unit_num}')

        start_datetime_str = datetime.strftime(self.start_date, '%d %b %y %H:%M')
        end_datetime_str = datetime.strftime(self.end_date, '%d %b %y %H:%M')
        result_str = f'{start_datetime_str} - {end_datetime_str}\n <b>{", ".join(result_lst)}</b>'
        return result_str

    def get_remains(self, **time_period):
        '''Additionally subtract time_period: years, months etc.)'''
        remains = (self.end_date - relativedelta(time_period) - self.start_date)
        return remains

    def get_r_delta(self):
        '''
        Get the relativedelta object between the end date and start date.
        relativedelta(months, days, hours, minutes, seconds, microseconds); optional - weeeks
        '''
        r_delta = relativedelta(self.end_date, self.start_date)
        return r_delta

    def get_delta(self):
        '''
        Get the timedelta object between the end date and start date.
        Total days or total seconds
        '''
        delta = self.end_date - self.start_date
        return delta

    def parse_relativedelta(self, relativedelta: relativedelta) -> list:
        '''
        Parse the relativedelta object and return a list of human-readable strings.
        :param relativedelta: relativedelta(end, start) function result as a relativedelta object:
        `relativedelta(months=+4, days=+21, hours=+3, minutes=+34)`
        :return: List of human-readable list containing the string of all non zero time units:
        `['Months: 4', 'Days: 21', 'Hours: 3', 'Minutes: 16']`
        '''
        result_list = []

        # get the value of the current time unit from the relativedelta object
        # if the value non zero, it added to result list in the format: "Time Unit name: value"
        for time_unit_name in self.UNITS:
            if time_unit_name == 'weeks':
                continue
            time_unit_num = getattr(relativedelta, time_unit_name)
            if time_unit_num:
                result_list.append(f'{time_unit_name.capitalize()}: {time_unit_num}')
        return result_list

    def __str__(self) -> str:
        '''
        Quick_count (dateutil.relativedelta)
        :return: string with a number of years-months-weeks-days-hours-minutes depending on the time interval size
        `Years: 14, Months: 7, Days: 24, Minutes: 45`
        '''
        output_list = self.parse_relativedelta(self._r_delta)
        print(f'Result: {output_list}')
        return ', '.join(output_list)

    def years(self):
        self._years = self._r_delta.years
        return self._years

    def months(self):
        if self._years is not None:
            self._months = self._r_delta.months
        else:
            self._months = self._r_delta.years * 12 + self._r_delta.months
        return self._months

    def weeks(self):
        if self._months is not None:
            # remains = self.get_remains(years=self._years, months=self._months)
            # self._weeks = remains.days // 7
            # or self._weeks = self._r_delta.days // 7
            self._weeks = self._r_delta.weeks  # dateutil method
        elif self._years is not None:
            # remains = self.get_remains(years=self._years)
            remains = self.get_remains(years=self._r_delta.years)
            self._weeks = remains.days // 7
        else:
            self._weeks = self._delta.days // 7
        return self._weeks

    def days(self):
        if self._weeks is not None:
            self._days = self._r_delta.days % 7
        elif self._months is not None:
            self._days = self._r_delta.days
        elif self._years is not None:
            remains = self.get_remains(years=self._r_delta.years)
            self._days = remains.days
        else:
            self._days = self._delta.days
        return self._days

    def hours(self):
        if self._days is not None:
            self._hours = self._r_delta.hours
        elif self._weeks is not None:
            self._hours = self._r_delta.days % 7 * 24 + self._r_delta.hours
        elif self._months is not None:
            self._hours = self._r_delta.days * 24 + self._r_delta.hours
            # TODO: Попробовать такой способ
            # remains = self.get_remains(years=self._r_delta.years, months=self._r_delta.months)
            # or remains = self.get_remains(years=self._years, months=self._months)
            # self._hours = remains.total_seconds() // 3600
        elif self._years is not None:
            remains = self.get_remains(years=self._r_delta.years)
            self._hours = remains.total_seconds() // 3600
        else:
            self._hours = self._delta.total_seconds() // 3600
        return self._hours

    def minutes(self):
        if self._hours is not None:
            self._minutes = self._r_delta.minutes
        elif self._days is not None:
            self._minutes = self._r_delta.hours * 60 + self._r_delta.minutes
        elif self._weeks is not None:
            self._minutes = (self._r_delta.days % 7 * 24 * 60) + \
                (self._r_delta.hours * 60) + self._r_delta.minutes
        elif self._months is not None:
            self._minutes = (self._r_delta.days * 24 * 60) + \
                (self._r_delta.hours * 60) + self._r_delta.minutes
        elif self._years is not None:
            remains = self.get_remains(years=self._r_delta.years)
            self._minutes = remains.total_seconds() // 60
        else:
            self._minutes = self._delta.total_seconds() // 60
        return self._minutes
