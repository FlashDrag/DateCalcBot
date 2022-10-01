"""Калькулятор времени"""
# вычислять таймзону в боте и парсить с помощью pytz
from dateutil import relativedelta
import datetime

# datetime.datetime.now(tz: _TzInfo | None = ...) -> date

# dic = {'Years': '%Y', 'Months': '%m', 'Weeks': ''}

# выберите что нужно посчитать (user выбирает нажатием инлайн кнопок, выбор добавляеться в список user_choice)
user_choice = 'minutes'

if 'Hours' in user_choice or 'Minutes' in user_choice:
    """Дата и время"""
    # От которой даты и времени считаем? `Текущее` | `Ввести дату и время`
    choice_start_date = 'Текущее'
    if choice_start_date == 'Текущее':
        start_date = datetime.datetime.now()
    else:
        # введите дату и время в формате `число-месяц-год время`, например 5-07-2021 14.00
        input_start_date = '5-07-2021 14.00'
        try:
            start_date = datetime.datetime.strptime(input_start_date, '%d-%m-%Y %H:%M')
        except Exception as e:
            print(e, '\nНеккоректный ввод, повторите еще раз в заданном формате')

    # _ДО_ которой даты и времени считаем? `Текущая` | `Ввести дату и время`
    choice_end_date = 'Текущая'
    if choice_end_date == 'Текущая':
        end_date = datetime.datetime.now()
    else:
        # Введите конечную дату и время `число-месяц-год`, например 5-07-2023 15.00
        input_end_date = '5-07-2023 15.00'
        try:
            end_date = datetime.datetime.strptime(input_end_date, '%d-%m-%Y %H:%M')
        except Exception as e:
            print(e, '\nНеккоректный ввод, повторите еще раз в заданном формате')
else:
    """Только дата"""
    # _ОТ_ которой даты? `Текущая` | `Ввести дату`
    choice_start_date = 'Текущая'
    if choice_start_date == 'Текущая':
        start_date = datetime.datetime.now()
    else:
        # введите дату `число-месяц-год`, например 5-07-2021
        input_start_date = '5-07-2021'
        try:
            start_date = datetime.datetime.strptime(input_start_date, '%d-%m-%Y')
        except Exception as e:
            print(e, '\nНеккоректный ввод, повторите еще раз в заданном формате')

    # _ДО_ которой даты? `Текущая` | `Ввести дату`
    choice_end_date = 'Ввести дату'
    if choice_end_date == 'Текущая':
        end_date = datetime.datetime.now()
    else:
        # Введите конечную дату `число-месяц-год`, например 5-07-2023
        input_end_date = '5-07-2023'
        try:
            end_date = datetime.datetime.strptime(input_end_date, '%d-%m-%Y')
        except Exception as e:
            print(e, '\nНеккоректный ввод, повторите еще раз в заданном формате')


start_date = datetime.datetime.now()
end_date = datetime.datetime.strptime('1-01-2024', '%d-%m-%Y')

# Get the relativedelta between two dates
if start_date > end_date:
    r_delta = relativedelta.relativedelta(start_date, end_date)
    delta = start_date - end_date
else:
    r_delta = relativedelta.relativedelta(end_date, start_date)
    delta = end_date - start_date
# print(delta)

if 'years' in user_choice and user_choice.count('|') == 0:
    res = (r_delta.years,)
elif 'years|months' in user_choice and user_choice.count('|') == 1:
    res = r_delta.years, r_delta.months
elif 'years|months|weeks' in user_choice and user_choice.count('|') == 2:
    res = r_delta.years, r_delta.months, r_delta.weeks
elif 'years|months|weeks|days' in user_choice and user_choice.count('|') == 3:
    res = r_delta.years, r_delta.months, r_delta.days // 7, r_delta.days % 7
elif 'years|months|weeks|days|hours' in user_choice and user_choice.count('|') == 4:
    res = r_delta.years, r_delta.months, r_delta.days // 7, r_delta.days % 7, r_delta.hours
elif 'years|months|weeks|days|hours|minutes' in user_choice and user_choice.count('|') == 5:
    res = r_delta.years, r_delta.months, r_delta.days // 7, r_delta.days % 7, r_delta.hours, r_delta.minutes

elif 'years|months|days'
elif 'years|months|days|hours'
elif 'years|months|days|hours|minutes'

elif 'years|months|hours'
elif 'years|months|hours|minutes'

elif 'years|months|minutes'

elif 'years|weeks' in user_choice and user_choice.count('|') == 1:
    res = r_delta.years, delta.days % 365 // 7
elif 'years|weeks|days' in user_choice and user_choice.count('|') == 2:
    res = r_delta.years, delta.days % 365 // 7, delta.days % 365 % 7
elif 'years|weeks|days|hours' in user_choice and user_choice.count('|') == 3:
    res = r_delta.years, delta.days % 365 // 7, delta.days % 365 % 7, r_delta.hours
elif 'years|weeks|days|hours|minutes' in user_choice and user_choice.count('|') == 4:
    res = r_delta.years, delta.days % 365 // 7, delta.days % 365 % 7, r_delta.hours, r_delta.minutes

elif 'years|weeeks|hours'
elif 'years|weeeks|hours|minutes'

elif 'years|weeeks|minutes'

elif 'years|days' in user_choice and user_choice.count('|') == 1:
    res = r_delta.years, delta.days % 365
elif 'years|days|hours' in user_choice and user_choice.count('|') == 2:
    res = r_delta.years, delta.days % 365, r_delta.hours
elif 'years|days|hours|minutes' in user_choice and user_choice.count('|') == 3:
    res = r_delta.years, delta.days % 365, r_delta.hours, r_delta.minutes

elif 'years|days|minutes'

elif 'years|hours' in user_choice and user_choice.count('|') == 1:
    res = r_delta.years, delta.days % 365 * 24
elif 'years|hours|minutes' in user_choice and user_choice.count('|') == 2:
    res = r_delta.years, delta.days % 365 * 24, r_delta.minutes

elif 'years|minutes' in user_choice and user_choice.count('|') == 1:
    res = r_delta.years, (delta.days % 365 * 24 * 60) + (r_delta.hours * 60) + r_delta.minutes


elif 'months' in user_choice and user_choice.count('|') == 0:
    res = ((r_delta.months + (r_delta.years * 12)),)
elif 'months|weeks' in user_choice and user_choice.count('|') == 1:
    res = r_delta.months + (r_delta.years * 12), r_delta.weeks
elif 'months|weeks|days' in user_choice and user_choice.count('|') == 2:
    res = r_delta.months + (r_delta.years * 12), r_delta.days // 7, r_delta.days % 7
elif 'months|weeks|days|hours' in user_choice and user_choice.count('|') == 3:
    res = r_delta.months + (r_delta.years * 12), r_delta.days // 7, r_delta.days % 7, r_delta.hours
elif 'months|weeks|days|hours|minutes' in user_choice and user_choice.count('|') == 4:
    res = r_delta.months, r_delta.days // 7, r_delta.days % 7, r_delta.hours, r_delta.minutes

elif 'months|weeks|hours'
elif 'months|weeks|hours|minutes'

elif 'months|weeks|minutes'

elif 'months|days' in user_choice and user_choice.count('|') == 1:
    res = r_delta.months + (r_delta.years * 12), r_delta.days
elif 'months|days|hours' in user_choice and user_choice.count('|') == 2:
    res = r_delta.months + (r_delta.years * 12), r_delta.days, r_delta.hours
elif 'months|days|hours|minutes' in user_choice and user_choice.count('|') == 3:
    res = r_delta.months + (r_delta.years * 12), r_delta.days, r_delta.hours, r_delta.minutes

elif 'months|days|minutes'

elif 'months|hours' in user_choice and user_choice.count('|') == 1:
    res = r_delta.months + (r_delta.years * 12), r_delta.days * 24
elif 'months|hours|minutes' in user_choice and user_choice.count('|') == 2:
    res = r_delta.months + (r_delta.years * 12), r_delta.days * 24, r_delta.minutes

elif 'months|minutes' in user_choice and user_choice.count('|') == 1:
    res = r_delta.months + (r_delta.years * 12), r_delta.days * 24 * 60 + r_delta.minutes


elif 'days' in user_choice and user_choice.count('|') == 0:
    res = (delta.days,)
elif 'days|hours' in user_choice and user_choice.count('|') == 1:
    res = delta.days, r_delta.hours
elif 'days|hours|minutes' in user_choice and user_choice.count('|') == 2:
    res = delta.days, r_delta.hours, r_delta.minutes

elif 'days|minutes' in user_choice and user_choice.count('|') == 1:
    res = delta.days, r_delta.hours * 60 + r_delta.minutes


elif 'hours' in user_choice and user_choice.count('|') == 0:
    res = (delta.days * 24,)
elif 'hours|minutes' in user_choice and user_choice.count('|') == 1:
    res = delta.days * 24, r_delta.minutes


elif 'minutes' in user_choice and user_choice.count('|') == 0:
    res = (delta.days * 24 * 60,)


user_choice_parser = user_choice.split('|')
print(dict(zip(user_choice_parser, res)))

