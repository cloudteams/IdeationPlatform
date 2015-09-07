__author__ = 'dipap'


DATABASE_CONNECTION_TYPES = [
    ('django.db.backends.sqlite3', 'SQLite3 file'),
    ('django.db.backends.mysql', 'MySQL'),

    # TODO: expand connection type list
]

AGGREGATE_LIST = [
    ('', ''),
    ('avg', 'Average'),
    ('sum', 'Sum'),

    # TODO: expand aggregate list
]

PROVIDER_PLUGINS = [
    # providers.Person
    ('^Person.first_name', 'Random name', [
        ('gender', 'The gender of this person'),
        ('male_val', 'Male gender value'),
        ('female_val', 'Female gender value'),
    ]),
    ('^Person.last_name_initial', 'Random last name (initial)'),

    # providers.Ranges
    ('^Ranges.from_int_value', 'Int value to range', [
        ('ranges', 'A set of ranges (e.g 1~10|11~20|21~30). Can also contain names like 1~10=Low'),
        ('value', 'The value that must be matched with the appropriate range'),
    ]),
    ('^Ranges.from_float_value', 'Float value to range', [
        ('ranges', 'A set of ranges (e.g 1~10|10~20|20~30). Can also contain names like 1~10=Low. Top limit of each range is NOT inclusive'),
        ('value', 'The value that must be matched with the appropriate range'),
    ]),
]
