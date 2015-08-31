__author__ = 'dipap'

from util import configuration


class ConnectionManager:
    """
    The connection manager handles connections to different databases manifested in the test_config.json file
    """
    def __init__(self):
        self.connections = []

        # create connection to all databases & save them
        for conn_info in configuration.data['sites'][0]['connections']:
            db = {'ID': conn_info['ID']}
            if conn_info['ENGINE'] == 'django.db.backends.sqlite3':
                import sqlite3
                conn = sqlite3.connect(conn_info['NAME'])
            else:
                raise Exception('Unsupported engine: ' + conn_info['ENGINE'])

            db['conn'] = conn

            # add to connections array
            self.connections.append(db)

connection_manager = ConnectionManager()