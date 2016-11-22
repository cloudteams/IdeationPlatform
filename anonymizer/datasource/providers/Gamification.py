import math

__author__ = 'dipap'


def xp_points_to_level(*args):
    xp_points = zip(*args)[0][0]
    if type(xp_points) == list:
        xp_points = xp_points[0]

    if not xp_points:
        return 0

    try:
        xp_points = int(xp_points)
    except ValueError:
        return 0

    level = int(math.floor(xp_points / 1000) + 1)

    if level <= 1:
        return 'New User'
    elif level <= 3:
        return 'Experienced User'
    else:
        return 'Veteran'
