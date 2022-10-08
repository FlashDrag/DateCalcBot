"""Калькулятор времени"""
# вычислять таймзону в боте и парсить с помощью pytz
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime

# datetime.now(tz: _TzInfo | None = ...) -> date


def get_date_time(date_time_input: str) -> datetime:
    '''
    Принимает либо слово `Текущее` либо дату и время в виде строки,
    парсит в `datetime` тип/формат
    '''
    if date_time_input == 'Текущее':
        date_time = datetime.now()
    else:
        date_time = parse(date_time_input, dayfirst=True)
    return date_time


def get_delta(start_date: datetime, end_date: datetime) -> tuple:
    ''' Get the relativedelta between two dates '''
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    delta = end_date - start_date
    r_delta = relativedelta(end_date, start_date)
    return delta, r_delta


def get_remains_from_year(start_date: datetime, end_date: datetime):
    '''Получить остаток 'timedelta' после вычитания полных лет'''
    r_delta = get_delta(start_date, end_date)[1]
    result = (end_date - relativedelta(years=r_delta.years) - start_date)
    return result


def calculate(user_choice: str, start_date: datetime, end_date: datetime) -> dict:
    '''
    Принимает:
    - Строку, которая обозначает комбинацию, которую нужно посчитать и вывести
    - Начальную и конечную даты (уже спарсинные, и провалидированные) в типе `datetime`
    Вывод:
    - Словарь с ключами с `user_choice` и значением c переменной `res`
    '''
    delta, r_delta = get_delta(start_date, end_date)
    year_remains = get_remains_from_year(start_date, end_date)

    if 'years' == user_choice:
        res = (r_delta.years,)
    elif 'years-months' == user_choice:
        res = r_delta.years, r_delta.months
    elif 'years-months-weeks' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.weeks
    elif 'years-months-weeks-days' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.weeks, r_delta.days % 7
    elif 'years-months-weeks-days-hours' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.weeks, r_delta.days % 7, r_delta.hours
    elif 'years-months-weeks-days-hours-minutes' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.weeks, r_delta.days % 7, r_delta.hours, r_delta.minutes

    elif 'years-months-days' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.days
    elif 'years-months-days-hours' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.days, r_delta.hours
    elif 'years-months-days-hours-minutes' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.days, r_delta.hours, r_delta.minutes

    elif 'years-months-hours' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.days * 24 + r_delta.hours
    elif 'years-months-hours-minutes' == user_choice:
        res = r_delta.years, r_delta.months, r_delta.days * \
            24 + r_delta.hours, r_delta.minutes

    elif 'years-months-minutes' == user_choice:
        res = r_delta.years, r_delta.months, \
            (r_delta.days * 24 + r_delta.hours) * 60 + r_delta.minutes

    elif 'years-weeks' == user_choice:
        res = r_delta.years, year_remains.days // 7
    elif 'years-weeks-days' == user_choice:
        res = r_delta.years, year_remains.days // 7, year_remains.days % 7
    elif 'years-weeks-days-hours' == user_choice:
        res = r_delta.years, year_remains.days // 7, year_remains.days % 7, r_delta.hours
    elif 'years-weeks-days-hours-minutes' == user_choice:
        res = r_delta.years, year_remains.days // 7, year_remains.days % 7, r_delta.hours, r_delta.minutes

    elif 'years-weeks-hours' == user_choice:
        res = r_delta.years, year_remains.days // 7, \
            (year_remains.days % 7 * 24) + r_delta.hours
    elif 'years-weeeks-hours-minutes' == user_choice:
        res = r_delta.years, year_remains.days // 7, \
            (year_remains.days % 7 * 24) + \
            r_delta.hours, r_delta.minutes

    elif 'years-weeks-minutes' == user_choice:
        res = r_delta.years, year_remains.days // 7, \
            (year_remains.days % 7 * 1440) + \
            (r_delta.hours * 60) + r_delta.minutes

    elif 'years-days' == user_choice:
        res = r_delta.years, year_remains.days
    elif 'years-days-hours' == user_choice:
        res = r_delta.years, year_remains.days, r_delta.hours
    elif 'years-days-hours-minutes' == user_choice:
        res = r_delta.years, year_remains.days, r_delta.hours, r_delta.minutes

    elif 'years-days-minutes' == user_choice:
        res = r_delta.years, year_remains.days, \
            r_delta.hours * 60 + r_delta.minutes

    elif 'years-hours' == user_choice:
        res = r_delta.years, year_remains.days * 24
    elif 'years-hours-minutes' == user_choice:
        res = r_delta.years, year_remains.days * 24, r_delta.minutes

    elif 'years-minutes' == user_choice:
        res = r_delta.years, (year_remains.days * 24 * 60) + \
            (r_delta.hours * 60) + r_delta.minutes

    # months
    elif 'months' == user_choice:
        res = (r_delta.months + (r_delta.years * 12)),
    elif 'months-weeks' == user_choice:
        res = r_delta.months + (r_delta.years * 12), r_delta.weeks
    elif 'months-weeks-days' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days // 7, r_delta.days % 7
    elif 'months-weeks-days-hours' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days // 7, r_delta.days % 7, r_delta.hours
    elif 'months-weeks-days-hours-minutes' == user_choice:
        res = r_delta.months, r_delta.days // 7, r_delta.days % 7, r_delta.hours, r_delta.minutes

    elif 'months-weeks-hours' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.weeks, r_delta.days % 7 * 24 + r_delta.hours
    elif 'months-weeks-hours-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), r_delta.weeks, \
            r_delta.days % 7 * 24 + r_delta.hours, r_delta.minutes

    elif 'months-weeks-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), r_delta.weeks, \
            (r_delta.days % 7 * 24 + r_delta.hours) * 60 + r_delta.minutes

    elif 'months-days' == user_choice:
        res = r_delta.months + (r_delta.years * 12), r_delta.days
    elif 'months-days-hours' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days, r_delta.hours
    elif 'months-days-hours-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days, r_delta.hours, r_delta.minutes

    elif 'months-days-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days, r_delta.hours * 60 + r_delta.minutes

    elif 'months-hours' == user_choice:
        res = r_delta.months + (r_delta.years * 12), r_delta.days * 24
    elif 'months-hours-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days * 24, r_delta.minutes

    elif 'months-minutes' == user_choice:
        res = r_delta.months + (r_delta.years * 12), \
            r_delta.days * 24 * 60 + r_delta.minutes

    # weeks
    elif 'weeks' == user_choice:
        res = delta.days // 7,
    elif 'weeks-days' == user_choice:
        res = delta.days // 7, delta.days % 7
    elif 'weeks-days-hours' == user_choice:
        res = delta.days // 7, delta.days % 7, r_delta.hours
    elif 'weeks-days-hours-minutes' == user_choice:
        res = delta.days // 7, delta.days % 7, r_delta.hours, r_delta.minutes

    elif 'weeks-hours' == user_choice:
        res = delta.days // 7, delta.days % 7 * 24 + r_delta.hours
    elif 'weeks-hours-minutes' == user_choice:
        res = delta.days // 7, delta.days % 7 * 24 + r_delta.hours, r_delta.minutes

    elif 'weeks-minutes' == user_choice:
        res = delta.days // 7, \
            (delta.days % 7 * 24 + r_delta.hours) * 60 + r_delta.minutes

    # days
    elif 'days' == user_choice:
        res = delta.days,
    elif 'days-hours' == user_choice:
        res = delta.days, r_delta.hours
    elif 'days-hours-minutes' == user_choice:
        res = delta.days, r_delta.hours, r_delta.minutes

    elif 'days-minutes' == user_choice:
        res = delta.days, r_delta.hours * 60 + r_delta.minutes

    # hours
    elif 'hours' == user_choice:
        res = delta.days * 24,
    elif 'hours-minutes' == user_choice:
        res = delta.days * 24, r_delta.minutes

    # minutes
    elif 'minutes' == user_choice:
        res = delta.days * 24 * 60,

    user_choice_parser = user_choice.split('-')
    return dict(zip(user_choice_parser, res))


