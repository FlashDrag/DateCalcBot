from datetime import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

def get_today():
    now = datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')
    return now


def get_new_year():
    current_year = date.today().year
    return f'1 Jan {current_year+1}'

a = get_today()
b = get_new_year()

start = parse(a)
end = parse(b)

print(relativedelta(end, start))