__author__ = 'dipap'


class InvalidArgumentsException(Exception):
    pass


def from_value(inclusive, *args):
    if len(*args) != 2:
        raise InvalidArgumentsException()

    ranges = zip(*args)[0][0].split(',')
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
                return '"%s"' % range_arr[1].split('=')[1]
            else:
                return '"%s..%s"' % (low, high)


def from_int_value(*args):
    return from_value(True, *args)


def from_float_value(*args):
    return from_value(False, *args)
