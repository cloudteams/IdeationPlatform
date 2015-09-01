__author__ = 'dipap'

import random
import string

# lists of names
male_names = ['Jack', 'John', 'Nick']
female_names = ['Stella', 'Rose', 'Eve', 'Kate']
all_names = male_names + female_names


class InvalidGenderOption(Exception):
    pass


class NoGenderOptions(Exception):
    pass


# provides a random first name
# can be based on gender
def first_name(*args):
    if len(args) > 0:
        # get gender information
        gender = zip(*args)[0][0]

        if len(*args) != 3:
            raise NoGenderOptions()

        gender_male = zip(*args)[1][0]
        gender_female = zip(*args)[2][0]
    else:
        gender = None

    # create the list of all usable names
    if not gender:
        names = all_names
    else:
        if gender == gender_male:
            names = male_names
        elif gender == gender_female:
            names = female_names
        else:
            raise InvalidGenderOption()

    # pick a random name
    return names[random.randint(1, len(names) - 1)]


# creates the initial of a surname
def last_name_initial(*args):
    return random.choice(string.ascii_letters).upper() + '.'
