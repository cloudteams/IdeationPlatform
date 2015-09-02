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
    ('^Person.first_name()', 'Random name'),
    ('^Person.first_name(Male,Male,Female)', 'Random male name'),
    ('^Person.first_name(Male,Male,Female)', 'Random female name'),
    ('^Person.last_name_initial()', 'Random last name (initial)'),
]
