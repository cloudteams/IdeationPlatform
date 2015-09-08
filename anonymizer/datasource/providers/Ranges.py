__author__ = 'dipap'


class InvalidArgumentsException(Exception):
    pass


def from_value(inclusive, *args):
    if len(*args) != 2:
        raise InvalidArgumentsException()

    ranges = zip(*args)[0][0].split('|')
    value = zip(*args)[1][0]

    for r in ranges:
        range_arr = r.split('..')
        low = range_arr[0]
        high = range_arr[1].split('=')[0]

        if inclusive:
            exp = (low == '' or float(low) <= value) and (high == '' or float(high) >= value)
        else:
            exp = (low == '' or float(low) <= value) and (high == '' or float(high) > value)

        if exp:
            if '=' in range_arr[1]:
                return '%s' % range_arr[1].split('=')[1]
            else:
                return '%s..%s' % (low, high)


# type helper to return the exact data type returned by a call to from_value
# the return type is based on the ranges in `*args`
def from_value__type(inclusive, *args):
    ranges = zip(*args)[0][0].split('|')
    return 'Scalar(%s)' % ','.join(ranges)


# int ranges are inclusive
# e.g 5..10 contains both 5 and 10
def from_int_value(*args):
    return from_value(True, *args)


def from_int_value__type(*args):
    return from_value__type(True, *args)


# float ranges are NOT inclusive
# e.g 5..10 contains all real numbers x where 5 <= x < 10
def from_float_value(*args):
    return from_value(False, *args)


def from_float_value__type(*args):
    return from_value__type(False, *args)
