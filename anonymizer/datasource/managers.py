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


class UnknownOperatorException(Exception):
    """
    Raised when a logical expression contains an invalid operator
    """
    pass


class Property:
    """
    A single property
    """
    def __init__(self, connection_manager, source, user_fk, name=None, tp=None, aggregate=None, label=None,
                 filter_by=True):
        self.connection_manager = connection_manager
        self.source = source
        self.table = source.split('@')[0].split('.')[0]
        self.column = source.split('@')[0].split('.')[1]
        self.aggregate = aggregate
        self.filter_by = filter_by

        if not name:
            self.name = self.column
            if aggregate:
                self.name += '__' + aggregate
        else:
            self.name = name

        self.label = label
        if not label:
            self.label = self.name

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
        self.user_pk = Property(self.connection_manager, self.configuration.data['sites'][0]['user_pk'], user_fk=None,
                                filter_by=False)

        self.properties = []

        for property_info in self.configuration.data['sites'][0]['properties']:
            if 'user_fk' in property_info:
                user_fk = property_info['user_fk']
            else:
                user_fk = None

            if 'aggregate' in property_info:
                aggregate = property_info['aggregate']
            else:
                aggregate = None

            if 'label' in property_info:
                label = property_info['label']
            else:
                label = property_info['name']

            if 'expose' in property_info:
                expose = property_info['expose']
            else:
                expose = True

            prop = Property(self.connection_manager, property_info['source'], user_fk=user_fk, name=property_info['name'],
                            tp=property_info['type'], aggregate=aggregate, label=label, filter_by=expose)

            self.properties.append(prop)

    def get_property_by_name(self, name):
        for prop in self.properties:
            if prop.name == name:
                return prop

        return None

    def list_filters(self):
        filters = []
        for p in self.properties:
            if p.filter_by:
                # ignore properties we're not allowed to filter by
                filters.append({
                    'name': p.name,
                    'label': p.label
                })

        return filters

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

        # removed non-exposed properties
        final_result = {}
        for key in result:
            prop = self.get_property_by_name(key)
            if prop.filter_by:
                final_result[key] = result[prop.name]

        return final_result

    def matches(self, val, filter_exp):
        """
        Checks if the value `val` follows the filter expression
        E.g val = "5", filter_exp = ">10" returns false
        """
        f_name = re.split('[=<>]', filter_exp)[0]
        operator = ''
        exp = ''

        for char in filter_exp[len(f_name):]:
            if not exp:
                if char in ['=', '<', '>', '!']:
                    operator += char
                else:
                    exp = char
            else:
                exp += char

        if (exp[0] == exp[-1] == '"') or (exp[0] == exp[-1] == "'"):
            exp = exp[1:-1]

        if operator == '=':
            return val == exp
        elif operator == '!=':
            return val != exp
        elif operator == '>':
            return val > exp
        elif operator == '>=':
            return val >= exp
        elif operator == '<':
            return val < exp
        elif operator == '<=':
            return val <= exp
        else:
            raise UnknownOperatorException(operator)

    def filter_by_generated(self, results, generated_filters):
        for g_filter in generated_filters:
            f_name = re.split('[=<>]', g_filter)[0]
            prop = self.get_property_by_name(f_name)

            if prop.is_generated():
                new_results = []
                for result in results:
                    if self.matches(result[prop.name], g_filter):
                        new_results.append(result)

                results = new_results

        return results

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

        # construct group by clause
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
            filters = filters.replace(' and ', ' AND ').split(' AND ')

        # separate filters between those on simple columns and those on aggregates
        filters_generated = []
        filters_concrete = []
        filters_aggregate = []
        for f in filters:
            prop = self.get_property_by_name(re.split('[=<>]', f)[0])
            if prop.is_generated():
                filters_generated.append(f)
            elif prop.aggregate is None:
                filters_concrete.append(f)
            else:
                filters_aggregate.append(f)

        # construct where clause
        if filters_concrete:
            where_clause = 'WHERE ' + ' AND '.join(filters_concrete)
            query += where_clause

        # construct group by clause
        group_by = ' GROUP BY ' + self.user_pk.full()
        query += group_by

        # aggregate filters must go after the group by in the `having` clause
        if filters_aggregate:
            having_clause = ' HAVING ' + ' AND '.join(filters_aggregate)
            query += having_clause

        # execute query & get results
        result = [self.info(row) for row in self.user_pk.connection.execute(query).fetchall()]

        # filter by generated fields & return result
        return self.filter_by_generated(result, filters_generated)

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
    def __init__(self, config_file='', from_str=''):
        if config_file:
            from_str = open(config_file).read()

        self.config = Configuration(from_str=from_str)
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

    def count(self, filters=None):
        if filters:
            qs = self.pm.filter(filters)
        else:
            qs = self.pm.all()

        return len(qs)

    def list_filters(self):
        return self.pm.list_filters()

    def list_properties(self):
        return self.pm.list_properties()