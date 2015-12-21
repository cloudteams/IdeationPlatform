__author__ = 'dipap'

import sqlite3
from mysql.connector import connect as mysql_connect
import psycopg2


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

        if self.is_sqlite3() or self.is_mysql() or self.is_postgres():
            pass
        else:
            raise UnsupportedEngine('Unsupported engine: ' + self.engine)

    def is_sqlite3(self):
        return self.engine == 'django.db.backends.sqlite3'

    def is_mysql(self):
        return self.engine == 'django.db.backends.mysql'

    def is_postgres(self):
        return self.engine == 'django.db.backends.psycopg2'

    def execute(self, query):
        """
        Create new cursor & execute the given query
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print(e)
            self.conn.rollback()

        return cursor

    def commit(self):
        """
        Commits the cursor
        """
        self.conn.commit()

    def tables(self):
        """
        :return: a list of all tables in this connection
        """
        if self.is_sqlite3():
            query = 'SELECT name FROM sqlite_master WHERE type=\'table\';'
        elif self.is_mysql():
            query = 'SHOW TABLES;'
        elif self.is_postgres():
            query = 'SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = \'public\';'

        return self.execute(query).fetchall()

    def primary_key_of(self, table_name):
        """
        :return: the primary key of this table
        """
        if self.is_sqlite3():
            query = "PRAGMA table_info('%s')" % table_name
            for row in self.execute(query).fetchall():
                if row[5]:  # 5th column is the `pk`
                    return '%s.%s@%s' % (table_name, row[1], self.id)

            raise ValueError('Could not find primary key of table "%s"' % table_name)
        elif self.is_mysql():
            query = "SHOW INDEX FROM %s where Key_name='PRIMARY'" % table_name
            row = self.execute(query).fetchone()
            return '%s.%s@%s' % (table_name, row[4], self.id)
        elif self.is_postgres():
            query = """
                SELECT
                c.column_name
                FROM
                information_schema.table_constraints tc
                JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
                JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
                WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '%s';
            """ % table_name

            row = self.execute(query).fetchone()
            return '%s.%s@%s' % (table_name, row[0], self.id)

    def get_data_properties(self, table_name, from_related=False):
        """
        If from_related is set to true, columns from other tables pointing to [table_name] will also be included
        :return: (all non-auto increment columns of table, all foreign key pairs)
        """
        result = []

        # check on which
        tables = [table_name]
        relationships = []
        if from_related:
            res = self.get_related_tables(table_name, already_accessed=[table_name])
            tables += res[0]
            relationships += res[1]

        tables = list(set(tables))
        # look for columns in the table(s)
        for table in tables:
            if self.is_sqlite3():
                query = "PRAGMA table_info('%s')" % table
                for row in self.execute(query).fetchall():
                    result.append((row[1], row[2], '%s.%s@%s' % (table, row[1], self.id)))

            elif self.is_mysql():
                query = "SHOW COLUMNS FROM %s;" % table
                for row in self.execute(query).fetchall():
                    if ('auto' not in row[5]) and ('MUL' not in row[3]):
                        result.append((row[0], row[1], '%s.%s@%s' % (table, row[0], self.id)))

            elif self.is_postgres():
                query = """
                    SELECT information_schema.columns.column_name, information_schema.columns.data_type
                    FROM information_schema.columns
                    WHERE information_schema.columns.table_name = '%s'
                    EXCEPT
                    SELECT information_schema.columns.column_name, information_schema.columns.data_type
                    FROM information_schema.columns
                    JOIN information_schema.table_constraints AS tc
                        ON tc.table_name = information_schema.columns.table_name
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name AND kcu.column_name = information_schema.columns.column_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE information_schema.columns.table_name = '%s' AND (constraint_type = 'FOREIGN KEY' OR (COALESCE(information_schema.columns.column_default, '') LIKE 'nextval%%'));
                """ % (table, table)
                for row in self.execute(query).fetchall():
                    result.append((row[0], row[1], '%s.%s@%s' % (table, row[0], self.id)))

        # save detected foreign keys
        return result, relationships

    def get_foreign_key_between(self, from_table, to_table):
        if self.is_sqlite3():
            query = "PRAGMA foreign_key_list('%s')" % from_table
            for row in self.execute(query).fetchall():
                if row[2].lower() == to_table.lower():
                    return '%s.%s@%s' % (from_table, row[3], self.id)

            return None

        elif self.is_mysql():
            query = """
                SELECT COLUMN_NAME
                FROM
                    information_schema.KEY_COLUMN_USAGE
                WHERE
                    TABLE_NAME = '%s' AND
                    REFERENCED_TABLE_NAME = '%s'
            """ % (from_table, to_table)

            return '%s.%s@%s' % (from_table, self.execute(query).fetchone()[0], self.id)

        elif self.is_postgres():
            query = """
                SELECT
                    tc.constraint_name, tc.table_name, kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='%s' AND ccu.table_name='%s';
            """ % (from_table, to_table)

            row = self.execute(query).fetchone()
            if not row:
                return None

            return '%s.%s@%s' % (from_table, row[2], self.id)

    def get_related_tables(self, table_name, already_accessed=None):
        """
        :param table_name: The name of the table that is examined
        :param already_accessed: The list of table names that have already been examined
        :return: A list of tuples (table_name, through_property) that can reach/be reached on this table
        """
        if not already_accessed:
            already_accessed = [table_name]

        table_pk = self.primary_key_of(table_name).split('@')[0]
        conn = self.primary_key_of(table_name).split('@')[1]
        relationships = []
        tables = []

        if self.is_sqlite3():
            # foreign keys FROM table_name
            query = "PRAGMA foreign_key_list('%s')" % table_name
            for row in self.execute(query).fetchall():
                tables.append(row[2])
                from_key = '%s.%s' % (table_name, row[3])
                to_key = '%s.%s' % (row[2], row[4])

                relationships.append((row[2], from_key, to_key))

            # foreign keys TO table_name
            # no automated way - we have to go through every table
            result = []
            for joined_table in self.tables():
                if joined_table not in result:
                    query = "PRAGMA foreign_key_list('%s')" % joined_table[0]

                    is_joined = False
                    for row in self.execute(query).fetchall():
                        if row[2].lower() == table_name.lower():  # 2nd column is target table
                            is_joined = True
                            break

                    if is_joined:
                        tables.append(joined_table[0])
                        relationships.append((joined_table[0], table_pk, '%s.%s' % (joined_table[0], row[3])))

        elif self.is_mysql():
            query = """
                SELECT DISTINCT TABLE_NAME, COLUMN_NAME, REFERENCED_COLUMN_NAME
                FROM
                  information_schema.KEY_COLUMN_USAGE
                WHERE
                  REFERENCED_TABLE_NAME = '%s'
            """ % table_name
            for row in self.execute(query).fetchall():
                if row[0]:
                    tables.append(row[0])
                    from_key = '%s.%s' % (table_name, row[2])
                    to_key = '%s.%s' % (row[0], row[1])
                    relationships.append((row[0], from_key, to_key))

            query = """
                SELECT DISTINCT REFERENCED_TABLE_NAME, COLUMN_NAME, REFERENCED_COLUMN_NAME
                FROM
                  information_schema.KEY_COLUMN_USAGE
                WHERE
                  TABLE_NAME = '%s'
            """ % table_name
            for row in self.execute(query).fetchall():
                if row[0]:
                    tables.append(row[0])
                    from_key = '%s.%s' % (row[1], table_name)
                    to_key = '%s.%s' % (row[0], row[2])
                    relationships.append((row[0], from_key, to_key))

        elif self.is_postgres():
            # foreign keys referencing table_name
            query = """
                SELECT DISTINCT information_schema.columns.table_name, information_schema.columns.column_name, ccu.column_name
                FROM information_schema.columns
                JOIN information_schema.table_constraints AS tc
                    ON tc.table_name = information_schema.columns.table_name
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name AND kcu.column_name = information_schema.columns.column_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' AND (ccu.table_name = '%s')
            """ % table_name
            for row in self.execute(query).fetchall():
                tables.append(row[0])
                from_key = '%s.%s' % (table_name, row[2])
                to_key = '%s.%s' % (row[0], row[1])
                relationships.append((row[0], from_key, to_key))

            # foreign keys referenced by table_name
            query = """
                SELECT DISTINCT ccu.table_name, information_schema.columns.column_name, ccu.column_name
                FROM information_schema.columns
                JOIN information_schema.table_constraints AS tc
                    ON tc.table_name = information_schema.columns.table_name
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name AND kcu.column_name = information_schema.columns.column_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' AND (information_schema.columns.table_name = '%s')
            """ % table_name
            for row in self.execute(query).fetchall():
                tables.append(row[0])
                from_key = '%s.%s' % (row[0], row[2])
                to_key = '%s.%s' % (table_name, row[1])
                relationships.append((row[0], from_key, to_key))

        # recursively search all referenced tables
        final_result = []
        for table in tables:
            if table not in already_accessed:
                final_result.append(table)
                old_already_accessed = already_accessed[:]
                already_accessed.append(table)
                res = self.get_related_tables(table, already_accessed)

                # filter out relations
                final_result += res[0]
                for rel in res[1]:
                    if rel[0] not in old_already_accessed:
                        relationships.append(rel)

        # add connection string
        final_relationships = []
        for relationship in relationships:
            rel_1 = relationship[1]
            if '@' not in rel_1:
                rel_1 += '@' + conn

            rel_2 = relationship[2]
            if '@' not in rel_2:
                rel_2 += '@' + conn

            final_relationships.append([
                relationship[0],
                rel_1,
                rel_2,
            ])

        # return all connected tables
        return final_result, final_relationships


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
            elif connection.is_postgres():
                conn = psycopg2.connect("host='%s' port='%s' user='%s' password='%s' dbname='%s'" %
                                        (conn_info['host'], conn_info['port'], conn_info['user'],
                                         conn_info['password'], conn_info['name']))
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


