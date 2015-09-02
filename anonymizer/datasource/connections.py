__author__ = 'dipap'

import sqlite3
from mysql.connector import connect as mysql_connect


class ConnectionManager:
    """
    The connection manager handles connections to different databases manifested in the test_config.json file
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.connections = []

        # create connection to all databases & save them
        for conn_info in self.configuration.data['sites'][0]['connections']:
            db = {
                'id': conn_info['id'],
                'engine': conn_info['engine'],
            }

            if conn_info['engine'] == 'django.db.backends.sqlite3':
                conn = sqlite3.connect(conn_info['name'])
            elif conn_info['engine'] == 'django.db.backends.mysql':
                conn = mysql_connect(host=conn_info['host'], port=conn_info['port'],
                                     user=conn_info['user'], password=conn_info['password'],
                                     database=conn_info['name'])
            else:
                raise Exception('Unsupported engine: ' + conn_info['ENGINE'])

            db['conn'] = conn

            # add to connections array
            self.connections.append(db)
