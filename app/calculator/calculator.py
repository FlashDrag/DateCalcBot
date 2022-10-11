from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime


class DT:
    def __init__(self, user_datetime_string: str):
        self.set_datetime(user_datetime_string)

    def get_datetime(self):
        return self.__datetime

    def set_datetime(self, value):
        dt = parse(value, dayfirst=True)  # params dayfirst or yearfirst set by Local, if the user showed his location
        self.__datetime = dt

    def __str__(self) -> str:
        res = datetime.strftime(self.get_datetime(), '%d %b %y %H:%M')  # set output string format by Local
        print(res)
        return res


class Calc:
    # TODO: сделать проверку по типу datetime
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

        self._r_delta = self.get_r_delta()
        self._delta = self.get_delta()

        self._years = None
        self._months = None
        self._weeks = None
        self._days = None
        self._hours = None
        self._minutes = None

    def get_remains(self, **time_period):
        '''Additionally subtract time_period: years, months etc.)'''
        remains = (self.end_date - relativedelta(time_period) - self.start_date)
        return remains

    def get_r_delta(self):
        '''relativedelta(months, days, hours, minutes, seconds, microseconds); optional - weeeks'''
        r_delta = relativedelta(self.end_date, self.start_date)
        return r_delta

    def get_delta(self):
        '''Total days or total seconds'''
        delta = self.end_date - self.start_date
        return delta

    def parse_relativedelta(self, relativedelta) -> list:
        '''
        Принимает результат ф-ции relativedelta(end, start):
        relativedelta(months=+4, days=+21, hours=+3, minutes=+34)
        Парсит в список строк:
        ['Months: 4', 'Days: 21', 'Hours: 3', 'Minutes: 16']
        '''
        attributes = ["years", "months", "days", "hours", "minutes"]
        result = []

        for attr in attributes:
            num = getattr(relativedelta, attr)  # получаем число по атрибуту
            if num:
                result.append(f'{attr.capitalize()}: {abs(num)}')
        return result

    def __str__(self) -> str:
        '''
        Quick_count (dateutil.relativedelta)
        Getting the number of years-months-weeks-days-hours-minutes depending on the time interval size
        Output example: `Years: 14, Months: 7, Days: 24, Minutes: 45`
        '''
        output_list = self.parse_relativedelta(self._r_delta)
        print(f'res: {output_list}')
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
