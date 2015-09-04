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
]
