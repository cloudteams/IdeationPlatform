__author__ = 'dipap'

from django.utils.timezone import now
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta


class InvalidBirthday(Exception):
    pass


def age_from_birthday(*args):
    if len(*args) != 1:
        raise ValueError('Exactly one argument (birthday) was expected, %d were found' % len(*args))

    birthday = zip(*args)[0][0]
    if not birthday:
        return None

    if type(birthday) == list:
        birthday = birthday[0]

    if type(birthday) == int:  # year
        birthday = datetime(year=birthday, month=1, day=1).replace(tzinfo=None)
    elif type(birthday) in [str, unicode]:  # timestamp
        try:
            birthday = parser.parse(birthday)
        except ValueError:
            raise InvalidBirthday('%s can not be parsed into a valid date' % birthday)

    return relativedelta(now().replace(tzinfo=None), birthday).years

DAY_PERIODS = [
    {'hour': 0, 'name': 'Night'},
    {'hour': 6, 'name': 'Morning'},
    {'hour': 12, 'name': 'Noon'},
    {'hour': 15, 'name': 'Afternoon'},
    {'hour': 19, 'name': 'Evening'},
    {'hour': 21, 'name': 'Night'},
]


def part_of_day(*args):
    if len(*args) != 1:
        raise ValueError('Exactly one argument (datetime) was expected, %d were found' % len(*args))

    t = zip(*args)[0][0]
    if not t:
        return None

    if type(t) != list:
        ts = [t]
    else:
        ts = t
        result = []

    for t in ts:
        if t:
            if type(t) != datetime:
                try:
                    t = parser.parse(t)
                except ValueError:
                    raise ValueError('%s can not be parsed into a valid datetime' % ts)

            pos = len(DAY_PERIODS) - 1
            for idx in range(len(DAY_PERIODS) - 1):
                if DAY_PERIODS[idx + 1]['hour'] > t.hour:
                    pos = idx
                    break

            r = DAY_PERIODS[pos]['name']
        else:
            r = None

        if type(ts) != list:
            return r
        else:
            result.append(r)

    return result
