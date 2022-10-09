def parse_relativedelta(relativedelta) -> list:
    '''
    Принимает результат ф-ции dateutil.relativedelta.relativedelta - (relativedelta(end, start)):
    relativedelta(months=+4, days=+21, hours=+3, minutes=+34)
    Парсит в список строк:
    ['Months: 4', 'Days: 21', 'Hours: 3', 'Minutes: 16']
    '''
    attributes = ["years", "months", "days", "hours", "minutes"]
    result = []

    for attr in attributes:
        num = eval(f'relativedelta.{attr}')  # получаем число по атрибуту
        if num:
            result.append(f'{attr.capitalize()}: {abs(num)}')

    return result
