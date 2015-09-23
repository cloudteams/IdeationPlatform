__author__ = 'dipap'

from django.utils.timezone import now
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

    if type(birthday) in [str, unicode]:
        try:
            birthday = parser.parse(birthday)
        except ValueError:
            raise InvalidBirthday('%s can not be parsed into a valid date' % birthday)

    return relativedelta(now().replace(tzinfo=None), birthday).years
