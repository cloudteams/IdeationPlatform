__author__ = 'dipap'


DATABASE_CONNECTION_TYPES = [
    ('django.db.backends.sqlite3', 'SQLite3 file'),
    ('django.db.backends.mysql', 'MySQL'),
    ('django.db.backends.psycopg2', 'Postgres'),

    # TODO: expand connection type list
]

AGGREGATE_LIST = [
    ('', ''),
    ('avg', 'Average'),
    ('sum', 'Sum'),
    ('count(DISTINCT @param)', 'Count'),
    ('GROUP_CONCAT', 'Concatenate'),

    ('to_char(@param, \'HH24\')', 'Hour from a datetime')
    # TODO: expand aggregate list
]

PROVIDER_PLUGINS = [
    # providers.Person
    {
        'source': '^Person.first_name',
        'label': 'Random name',
        'args': [
            ('gender', 'The gender of this person'),
            ('male_val', 'Male gender value'),
            ('female_val', 'Female gender value'),
        ],
        'type': 'VARCHAR(255)'
    },
    {
        'source': '^Person.last_name_initial',
        'label': 'Random last name (initial)',
        'type': 'VARCHAR(2)'
    },

    # providers.Ranges
    {
        'source': '^Ranges.from_int_value',
        'label': 'Int value to range',
        'args': [
            ('ranges', 'A set of ranges (e.g 1..10|11..20|21..30). Can also contain names like 1..10=Low'),
            ('value', 'The value that must be matched with the appropriate range')
        ],
        'type': '###',
    },
    {
        'source': '^Ranges.from_float_value',
        'label': 'Float value to range',
        'args': [
            ('ranges', 'A set of ranges (e.g 1..10|10..20|20..30). Can also contain names like 1..10=Low. Top limit of each range is NOT inclusive'),
            ('value', 'The value that must be matched with the appropriate range'),
        ],
        'type': '###',
    },

    # providers.Location
    {
        'source': '^Location.address_to_city',
        'label': 'Extracts the city from an address',
        'args': [
            ('address', 'Address'),
        ],
        'type': 'VARCHAR(255)',
    },
    {
        'source': '^Location.address_to_country',
        'label': 'Extracts the country from an address',
        'args': [
            ('address', 'Address'),
        ],
        'type': 'VARCHAR(255)',
    },
    {
        'source': '^Location.address_to_city_country',
        'label': 'Extracts the city and country from an address',
        'args': [
            ('address', 'Address'),
        ],
        'type': 'VARCHAR(255)',
    },

    # providers.Dates
    {
        'source': '^Dates.age_from_birthday',
        'label': 'Calculate age based on birthday',
        'args': [
            ('birthday', 'The birthday date'),
        ],
        'type': 'INT(11)',
    },
    {
        'source': '^Dates.part_of_day',
        'label': 'Find the part of the day based on a timestamp',
        'args': [
            ('timestamp', 'Timestamp'),
        ],
        'type': 'VARCHAR(255)',
    },
    {
        'source': '^Dates.part_of_day_from_hour',
        'label': 'Find the part of the day based on the hour',
        'args': [
            ('hour', '24-hour based value'),
        ],
        'type': 'VARCHAR(255)',
    },
]
