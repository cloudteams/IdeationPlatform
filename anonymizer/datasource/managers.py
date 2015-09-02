__author__ = 'dipap'

from util import Configuration
from connections import ConnectionManager
from pydoc import locate
import re


class PropertyManagerException(Exception):
    """
    Exceptions caused by the property manager
    """
    pass


class UserManagerException(Exception):
    """
    Exceptions caused by the user manager
    """
    pass


class ProviderNotFound(Exception):
    """
    A data provider described in the configuration was not found
    """
    pass


class ProviderMethodNotFound(Exception):
    """
    A method of a data provider described in the configuration was not found
    """
    pass


class PropertyNotFoundException(Exception):
    """
    Exception for when a property name described in the configuration is not found
    """
    pass


class Property:
    """
    A single property
    """
    def __init__(self, connection_manager, source, user_fk, name=None, tp=None, aggregate=None):
        self.connection_manager = connection_manager
        self.source = source
        self.table = source.split('@')[0].split('.')[0]
        self.column = source.split('@')[0].split('.')[1]
        self.aggregate = aggregate

        if not name:
            self.name = self.column
            if aggregate:
                self.name += '__' + aggregate
        else:
            self.name = name

        if tp:
            self.type = tp
        else:
            self.tp = 'string'

        if not self.is_generated():
            # find responsible db connection
            conn_name = source.split('@')[1]
            self.connection = connection_manager.get(conn_name)

            if user_fk:
                self.user_fk = Property(self.connection_manager, user_fk, user_fk=None)
            else:
                self.user_fk = None
        else:
            # load provider class
            cls_name = 'anonymizer.datasource.providers.' + self.source.split('.')[0][1:]
            cls = locate(cls_name)
            if not cls:
                raise ProviderNotFound('Provider ' + cls_name + ' was not found')

            # load provider class method
            fn_name = self.source.split('.')[1].split('(')[0]
            try:
                self.fn = getattr(cls, fn_name)
            except AttributeError:
                raise ProviderMethodNotFound('Provider method ' + fn_name + ' was not found')

    def is_generated(self):
        return self.source[0] in ['^']

    def full(self):
        result = self.table + '.' + self.column
        if self.aggregate:
            result = self.aggregate + '(' + result + ')'

        return result


class PropertyManager:
    """
    The manager for all properties
    """
    def __init__(self, connection_manager, configuration):
        self.connection_manager = connection_manager
        self.configuration = configuration
        self.user_pk = Property(self.connection_manager, self.configuration.data['sites'][0]['user_pk'], user_fk=None)

        self.properties = [self.user_pk]

        for property_info in self.configuration.data['sites'][0]['properties']:
            if 'user_fk' in property_info:
                user_fk = property_info['user_fk']
            else:
                user_fk = None

            if 'aggregate' in property_info:
                aggregate = property_info['aggregate']
            else:
                aggregate = None

            prop = Property(self.connection_manager, property_info['source'], user_fk=user_fk, name=property_info['name'],
                            tp=property_info['type'], aggregate=aggregate)

            self.properties.append(prop)

    def get_property_by_name(self, name):
        for prop in self.properties:
            if prop.name == name:
                return prop

        return None

    def info(self, row):
        idx = 0
        result = {}

        # fill property values from database
        for prop in self.properties:
            if not prop.is_generated():
                result[prop.name] = row[idx]
                idx += 1

        # generate other properties
        for prop in self.properties:
            if prop.is_generated():
                # get function argument
                fn_args = prop.source.split('.')[1].split('(')[1][:-1].split(',')

                # search for 'special' arguments the must be replaced
                # e.g property names like `@age`
                for idx, fn_arg in enumerate(fn_args):
                    if fn_arg:
                        # replace property names with their values
                        if fn_arg[0] == '@':
                            try:
                                fn_args[idx] = result[fn_arg[1:]]
                            except KeyError:
                                raise PropertyNotFoundException('Property "' + fn_arg[1:] + '" was not found.')

                # apply function and save the result
                result[prop.name] = prop.fn(fn_args)

        return result

    def query(self):
        select_clause = 'SELECT ' + \
                        ','.join([prop.full() + ' AS ' + prop.name for prop in self.properties if not prop.is_generated()]) + ' '

        from_clause = 'FROM {0} '.format(self.user_pk.table)

        # find all joins
        join_clause = ''
        for prop in self.properties:
            if not prop.is_generated():
                if prop.user_fk:
                    join_clause += 'LEFT OUTER JOIN {0} ON {1}={2} '\
                        .format(prop.table, prop.user_fk.full(), self.user_pk.full())

        # return the `all` query
        return select_clause + from_clause + join_clause

    def all(self):
        query = self.query()

        group_by = ' GROUP BY ' + self.user_pk.full()
        query += group_by

        # execute query & return results
        return [self.info(row) for row in self.user_pk.connection.execute(query).fetchall()]

    def filter(self, filters):
        if not filters:
            return self.all()

        query = self.query()

        # create where clause
        if not type(filters) == list:
            filters = [filters]

        # separate filters between those on simple columns and those on aggregates
        filters_concrete = [f for f in filters if self.get_property_by_name(re.split('[=<>]', f)[0]).aggregate is None]
        filters_aggegate = set(filters) - set(filters_concrete)

        # construct where clause
        where_clause = 'WHERE ' + ' AND '.join(filters_concrete)
        query += where_clause

        # construct group by clause
        group_by = ' GROUP BY ' + self.user_pk.full()
        query += group_by

        # aggregate filters must go after the group by in the `having` clause
        if filters_aggegate:
            having_clause = ' HAVING ' + ' AND '.join(filters_aggegate)
            query += having_clause

        # execute query & return results
        return [self.info(row) for row in self.user_pk.connection.execute(query).fetchall()]

    def get(self, pk):
        where_clause = 'WHERE {0}={1}'.format(self.user_pk.full(), pk)

        # construct full query
        query = self.query() + where_clause

        # execute query & return results
        return self.info(self.user_pk.connection.execute(query).fetchone())


class UserManager:
    """
    The User manager is responsible for fetching and filtering user information
    """
    def __init__(self, config_file):
        self.config = Configuration(config_file)
        self.cm = ConnectionManager(self.config.get_connection_info())
        self.pm = PropertyManager(self.cm, self.config)

    def get(self, pk):
        # Ensures the user exists
        query = "SELECT {0} AS pk FROM {1} WHERE pk={2}".format(self.pm.user_pk.full(), self.pm.user_pk.table, pk)
        result = self.pm.user_pk.connection.execute(query).fetchall()

        # check uniqueness
        if len(result) == 0:
            raise UserManagerException('User with id={0} does not exist'.format(pk))
        elif len(result) > 1:
            raise UserManagerException('More than one users with id={0} where found'.format(pk))

        return self.pm.get(pk)

    def filter(self, filters):
        return self.pm.filter(filters)

    def all(self):
        return self.pm.all()
