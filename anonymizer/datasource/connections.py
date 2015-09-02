__author__ = 'dipap'

import sqlite3
from mysql.connector import connect as mysql_connect


class UnsupportedEngine(Exception):
    pass


class ConnectionNotFound(Exception):
    pass


class Connection:
    """
    A single connection object to a database
    """

    def __init__(self, id, engine, conn=None):
        self.id = id
        self.engine = engine
        self.conn = conn

    def is_sqlite3(self):
        return self.engine == 'django.db.backends.sqlite3'

    def is_mysql(self):
        return self.engine == 'django.db.backends.mysql'

    def execute(self, query):
        # execute the query
        cursor = self.conn.cursor()
        cursor.execute(query)

        return cursor

    def tables(self):
        """
        :return: a list of all tables in this connection
        """
        if self.is_sqlite3():
            query = 'SELECT name FROM sqlite_master WHERE type=\'table\';'
        elif self.is_mysql():
            query = 'SHOW TABLES;'
        else:
            raise UnsupportedEngine('Unsupported engine: ' + self.engine)

        return self.execute(query).fetchall()


class ConnectionManager:
    """
    The connection manager handles connections to different databases manifested in the specified file
    """

    def __init__(self, connection_dict):
        self.connections = []

        # create connection to all databases & save them
        for conn_info in connection_dict:
            connection = Connection(id=conn_info['id'], engine=conn_info['engine'])

            if connection.is_sqlite3():
                conn = sqlite3.connect(conn_info['name'])
            elif connection.is_mysql():
                conn = mysql_connect(host=conn_info['host'], port=conn_info['port'],
                                     user=conn_info['user'], password=conn_info['password'],
                                     database=conn_info['name'])
            else:
                raise UnsupportedEngine('Unsupported engine: ' + conn_info['engine'])

            # save the connection object
            connection.conn = conn

            # add to connections array
            self.connections.append(connection)

    def get(self, connection_id):
        """
        :param connection_id: The id of the described connection
        :return:the connection with the described id
        """
        for connection in self.connections:
            # look for the connection
            if connection.id == connection_id:
                return connection

        raise ConnectionNotFound('connection with id="{0}" was not found in this configuration'.format(connection_id))


