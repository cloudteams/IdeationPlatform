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

        if self.is_sqlite3() or self.is_mysql():
            pass
        else:
            raise UnsupportedEngine('Unsupported engine: ' + self.engine)

    def is_sqlite3(self):
        return self.engine == 'django.db.backends.sqlite3'

    def is_mysql(self):
        return self.engine == 'django.db.backends.mysql'

    def execute(self, query):
        """
        Create new cursor & execute the giver query
        """
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

        return self.execute(query).fetchall()

    ###PRAGMA foreign_key_list('Running')
    def primary_key_of(self, table_name):
        """
        :return: the primary key of this table
        """
        if self.is_sqlite3():
            query = "PRAGMA table_info('%s')" % table_name
            for row in self.execute(query).fetchall():
                if row[5]:  # 5th column is the `pk`
                    return '%s.%s@%s' % (table_name, row[1], self.id)

            return None
        elif self.is_mysql():
            query = "SHOW INDEX FROM %s where Key_name='PRIMARY'" % table_name
            row = self.execute(query).fetchone()
            return '%s.%s@%s' % (table_name, row[4], self.id)

    def get_data_properties(self, table_name, from_related=False):
        """
        If from_related is set to true, columns from other tables pointing to [table_name] will also be included
        :return: all non-auto increment columns of table
        """
        result = []

        # check on which
        tables = [table_name]
        if from_related:
            tables += self.get_related_tables(table_name)

        # look for columns in the table(s)
        for table in tables:
            if self.is_sqlite3():
                query = "PRAGMA table_info('%s')" % table
                for row in self.execute(query).fetchall():
                    result.append((row[0], row[1]))
            elif self.is_mysql():
                query = "SHOW COLUMNS FROM %s;" % table
                for row in self.execute(query).fetchall():
                    if 'auto' not in row[5]:
                        result.append((row[0], row[1]))

        return result

    def get_related_tables(self, table_name):
        if self.is_sqlite3():
            result = []

            # no automated way - we have to go through every table
            for joined_table in self.tables():
                query = "PRAGMA foreign_key_list('%s')" % joined_table[0]

                is_joined = False
                for row in self.execute(query).fetchall():
                    if row[2] == table_name:  # 2nd column is target table
                        is_joined = True
                        break

                if is_joined:
                    result.append(joined_table[0])

            # return all connected tables
            return result
        elif self.is_mysql():
            query = """
                SELECT DISTINCT TABLE_NAME
                FROM
                  information_schema.KEY_COLUMN_USAGE
                WHERE
                  REFERENCED_TABLE_NAME = '%s'
            """ % table_name

            return [row[0] for row in self.execute(query).fetchall()]


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


