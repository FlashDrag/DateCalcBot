from datetime import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def get_today_string():
    now = datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')
    return now


def get_new_year():
    current_year = date.today().year
    return f'1 Jan {current_year+1}'


a = get_today_string()
b = get_new_year()

start = parse(a)
end = parse(b)

print(a, '-', b)
print(relativedelta(end, start))


def show_datetime_formates():
    s = "24.06.2022 - 1.01.2023\n" \
        "24 June 2022 - 1 Jan 2023\n" \
        "24.06.2022 - 1.01.2022 00:00\n" \
        "24 June 2022 20:00 - 1.01.2022 09:45\n" \
        "24 June 2022 12:00 - 1 Jan 2023 00:00\n"
    return s
