import asyncio

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from calculator.relativedelta_parser import parse_relativedelta

'''
Быстрый подсчет
Считает к-во лет-месяцев-недель-дней-часов-минут в зависимости от размера диапазона
Пользователь вводит две даты через знак тире между ними, и получает быстрый результат
'''


def quick_count(user_input_string: str) -> str:
    '''
    Принимает строку от юзера, парсит, вычисляет, и возвращает результат в виде строки
    Пример строки от юзера: `20.05.2003 23:15 - 14 Jan 2018`
    Пример вывода: `Years: 14, Months: 7, Days: 24, Minutes: 45`
    '''
    print(f'user_input_string: {user_input_string}')
    try:
        first, second = user_input_string.split('-')
    except Exception as e:

        print(f'Problem with spliting the user_input_string!\n '
              f'{type(e).__name__}: {e}')
        return 'Error: Wrong format'
    else:
        try:
            start = parse(first, dayfirst=True)
        except Exception as e:
            print(f'First part of the user_input_string if wrong'
                  f'{type(e).__name__}: {e}')
            return 'Error: Wrong format of your start date/time'
        else:
            try:
                end = parse(second, dayfirst=True)
            except Exception as e:
                print(f'First part of the user_input_string if wrong'
                      f'{type(e).__name__}: {e}')
                return 'Error: Wrong format of your end date/time'
            else:
                try:
                    delta = relativedelta(end, start)
                except Exception as e:
                    print(f'relativedelta\n'
                          f'{type(e).__name__}: {e}')
                    return 'Error: Wrong input, try again'
                else:
                    output_list = parse_relativedelta(delta)
                    print(f'res: {output_list}')
                    return ', '.join(output_list)


# print(quick_count('20.05.2003 23:15 - 14 Jan 2018'))
