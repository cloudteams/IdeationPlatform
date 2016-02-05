from datetime import datetime

__author__ = 'dipap'

from pydoc import locate
import hashlib
import re
import csv
import uuid


class PropertyManagerException(Exception):
    """
    Exceptions caused by the property manager
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


class InvalidPropertyConfiguration(Exception):
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

    def __init__(self, connection_manager, source, name=None, tp=None, aggregate=None, label=None,
                 filter_by=True, is_pk=False, options=None, options_auto=False):
        self.connection_manager = connection_manager
        self.source = source
        self.table = source.split('@')[0].split('.')[0]
        self.column = source.split('@')[0].split('.')[1]
        self.aggregate = aggregate
        self.filter_by = filter_by
        self.is_pk = is_pk

        if options and options_auto:
            raise InvalidPropertyConfiguration('Both options and options_auto can\'t be enabled at the same time.')

        self.options = options
        self.options_auto = options_auto

        if not name:
            self.name = self.column
            if aggregate:
                self.name += '__' + aggregate
        else:
            self.name = name

        self.label = label
        if not label:
            self.label = Property.humanize(self.name)

        if tp:
            self.tp = tp
        else:
            self.tp = 'VARCHAR'

        if not self.is_generated():
            # find responsible db connection
            conn_name = source.split('@')[1]
            self.connection = connection_manager.get(conn_name)
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

            # load arguments
            pos = self.source.find('(')
            args_str = self.source[pos + 1:-1]
            reader = csv.reader([args_str], delimiter=',')
            self.fn_args = next(reader)

            # if the type must be inferred execute the __type helper
            if self.tp == '###':
                try:
                    fn_type = getattr(cls, fn_name + '__type')
                except AttributeError:
                    raise ProviderMethodNotFound('Provider method ' + fn_name + ' declared dynamic type but function ' +
                                                 fn_name + '__type was not found')

                self.tp = fn_type(self.fn_args[:])

    @staticmethod
    def humanize(string):
        result = string.replace('_', ' ')
        return result[0].upper() + result[1:]

    def has_options(self):
        return self.options or self.options_auto

    def get_options(self):
        if not self.options:
            if self.is_generated():
                if 'Scalar(' in self.tp:
                    self.options = []
                    for r in self.tp.find('(')[:-1].split(','):
                        self.options.append((r, r))
                else:
                    self.options = []
            else:
                query = "SELECT DISTINCT {0} FROM {1}".format(self.column, self.table)
                rows = self.connection.execute(query)
                self.options = []
                for row in rows.fetchall():
                    option = row[0]
                    if option is None:
                        label = '<No value>'
                    else:
                        label = option
                    self.options.append((option, label))

        return self.options

    def is_generated(self):
        return self.source[0] in ['^']

    def full(self):
        result = self.table + '.' + self.column
        if self.aggregate:
            param_str = '@param'
            if param_str not in self.aggregate:  # plain style
                result = self.aggregate + '(%s)' % result
            else:  # @param style
                result = self.aggregate.replace(param_str, result)

        return result

    def matches(self, val, filter_exp):
        """
        Checks if the value `val` follows the filter expression
        E.g val = "5", filter_exp = ">10" returns false
        """
        f_name = re.split('[=!<>]', filter_exp)[0]
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

        # remove quotes
        if type(val) in [str, unicode]:
            if (val[0] == val[-1] == '"') or (val[0] == val[-1] == "'"):
                val = val[1:-1]

        if (exp[0] == exp[-1] == '"') or (exp[0] == exp[-1] == "'"):
            exp = exp[1:-1]

        if self.tp.lower().startswith('scalar'):
            ranges = self.tp.split('(')[1][:-1].split(',')

            for idx, r in enumerate(ranges):
                r_arr = r.split('=')
                if len(r_arr) == 1:
                    r_arr.append(r_arr[0])

                if val in r_arr:
                    val = idx
                if exp in r_arr:
                    exp = idx

            if type(val) != int:
                raise ValueError('Invalid option: ' + str(val))

            if type(exp) != int:
                raise ValueError('Invalid option: ' + str(exp))
        else:
            # read as number if possible
            try:
                exp = int(exp)
            except ValueError:
                try:
                    exp = float(exp)
                except ValueError:
                    pass

        # apply the operator
        if operator == '=':
            result = val == exp
        elif operator == '!=':
            result = val != exp
        elif operator == '>':
            result = val > exp
        elif operator == '>=':
            result = val >= exp
        elif operator == '<':
            result = val < exp
        elif operator == '<=':
            result = val <= exp
        else:
            raise UnknownOperatorException(operator)

        return result


class PropertyManager:
    """
    The manager for all properties
    """

    def __init__(self, connection_manager, configuration, token=None):
        self.connection_manager = connection_manager
        self.configuration = configuration
        self.user_pk = Property(self.connection_manager, self.configuration.data['sites'][0]['user_pk'], is_pk=True)

        self.properties = [self.user_pk]

        for property_info in self.configuration.data['sites'][0]['properties']:
            if property_info['source'] == self.user_pk.source:
                continue

            if 'aggregate' in property_info:
                aggregate = property_info['aggregate']
            else:
                aggregate = None

            label = property_info.get('label', None)

            if 'expose' in property_info:
                expose = property_info['expose']
            else:
                expose = True

            if 'options' in property_info:
                options = property_info['options']
            else:
                options = None

            if 'options_auto' in property_info:
                options_auto = property_info['options_auto']
            else:
                options_auto = False

            prop = Property(self.connection_manager, property_info['source'], name=property_info['name'],
                            tp=property_info['type'], aggregate=aggregate, label=label, filter_by=expose,
                            options=options, options_auto=options_auto)

            self.properties.append(prop)

        # group by tables
        self.group_tables = []
        for p in self.properties:
            if not p.aggregate and not p.is_generated():
                self.group_tables.append(p.table)

        # unique tables
        self.group_tables = list(set(self.group_tables))

        # generate manager token
        if not token:
            token = uuid.uuid4()
        self.token = token

        # save foreign keys
        self.foreign_keys = self.configuration.data['sites'][0]['foreign_keys']
        # query cache
        self._query = None

    def get_primary_key(self):
        for prop in self.properties:
            if prop.is_pk:
                return prop

        return None

    def get_property_by_name(self, name):
        for prop in self.properties:
            if prop.name == name:
                return prop

        return None

    def list_filters(self, ignore_options=False):
        filters = []
        for p in self.properties:
            if p.filter_by and not p.is_pk:
                # ignore properties we're not allowed to filter by
                filter = {
                    'name': p.name,
                    'label': p.label,
                    'type': p.tp,
                }

                if not ignore_options:
                    filter['has_options'] =  p.has_options
                    filter['get_options'] =  p.get_options

                filters.append(filter)

        return filters

    def get_dependencies(self, prop):
        if prop.is_generated():
            result = []

            for p_name in prop.fn_args:
                if p_name[0] == '@':
                    dep_prop = self.get_property_by_name(p_name[1:])
                    result.append(dep_prop)
                    # the dependencies of this dependency property are also mine
                    result += self.get_dependencies(dep_prop)

            return result
        else:
            return []

    def reduce(self, rows):
        """
        Expects the first row to be the user id and the result to be sorted
        """
        result_rows = []

        # detect which properties are NOT grouped by
        prop_idx = 0
        non_grouped = []
        for prop in self.properties:
            if not prop.is_generated():
                if (not prop.aggregate) and (prop.table != self.user_pk.table):
                    non_grouped.append(prop_idx)
                prop_idx += 1

        # find common users -- users should be sorted
        row_idx = -1
        idx = 0
        while idx < len(rows):
            if row_idx < 0 or rows[idx][0] != rows[row_idx][0]:  # new user
                row_idx = idx

                result_rows.append(list(rows[idx]))
                for prop_idx in non_grouped:
                    result_rows[-1][prop_idx] = [rows[idx][prop_idx]]
            else:  # same user
                for prop_idx in non_grouped:
                    result_rows[-1][prop_idx].append(rows[idx][prop_idx])

            # move to next row
            idx += 1

        return result_rows

    @staticmethod
    def apply(fn, fn_args):
        # TODO investigate differences between plain & compound evaluation
        """
        compound = False
        arg_lists = []
        for fn_arg in fn_args:
            if type(fn_arg) == list:
                n_of_recs = len(fn_args[0])
                for fn_arg in fn_args[1:]:
                    if type(fn_arg) == list:
                        if len(fn_arg) != n_of_recs:
                            raise ValueError('Can not apply function %s to variable length list %s' % (fn, fn_args))

            
                for i in range(0, n_of_recs):
                    arg_lists.append([fn_arg[i] for fn_arg in fn_args])
                print arg_lists
                return [fn(arg_list) for arg_list in arg_lists]
        """
        return fn(fn_args)

    def info(self, row, true_id=False):
        idx = 0
        result = {}

        # fill property values from database
        for prop in self.properties:
            if not prop.is_generated():
                if prop.is_pk:
                    # primary key
                    result[prop.name] = hashlib.sha1(str(self.token) + '###' + str(row[idx])).hexdigest()
                    if true_id:
                        result['__id__'] = row[idx]
                else:
                    # default property
                    result[prop.name] = row[idx]
                idx += 1

        # generate other properties
        for prop in self.properties:
            if prop.is_generated():
                fn_args = prop.fn_args[:]

                # search for 'special' arguments the must be replaced
                # e.g property names like `@age`
                for idx, fn_arg in enumerate(fn_args):
                    if fn_arg:
                        # replace property names with their values
                        if type(fn_arg) == str and fn_arg[0] == '@':
                            try:
                                fn_args[idx] = result[fn_arg[1:]]
                            except KeyError:
                                raise PropertyNotFoundException('Property "' + fn_arg[1:] + '" was not found.')

                # apply function and save the result
                # must apply multiple times for list arguments
                result[prop.name] = self.apply(prop.fn, fn_args)

        # removed non-exposed properties
        final_result = {}
        for key in result:
            if key == '__id__':
                final_result[key] = result[key]
            else:
                prop = self.get_property_by_name(key)
                if prop.filter_by:
                    final_result[key] = result[prop.name]

        return final_result

    def filter_by_generated(self, results, generated_filters):
        for g_filter in generated_filters:
            f_name = re.split('[=<>]', g_filter)[0]
            prop = self.get_property_by_name(f_name)

            if prop.is_generated():
                new_results = []
                for result in results:
                    if prop.matches(result[prop.name], g_filter):
                        new_results.append(result)

                results = new_results

        return results

    @staticmethod
    def insert_key(keys, new_key):
        """
        Inserts a foreign key at the correct position in the list, according to how they rely on each other
        """
        pos = len(keys)
        for idx, key in enumerate(keys):
            if new_key[0].lower() == key[1].split('.')[0].lower():
                pos = idx
                break

        keys.insert(pos - 1, new_key)

    def join_clause(self):
        """
        Returns the join clause of the query
        """
        # initially only the users table is ok because it's contained in the FROM clause
        current_tables = [self.user_pk.table]
        target_tables = list(set([prop.table for prop in self.properties if not prop.is_generated()]))
        current_keys = []

        while target_tables:  # while there are tables that are not covered by any join
            t = target_tables[0]

            if t in current_tables:
                target_tables = target_tables[1:]
                continue

            for key in self.foreign_keys:  # foreach possible join
                if key[0].lower() == t.lower():
                    current_tables.append(t)
                    self.insert_key(current_keys, key)
                    t2 = key[1].split('.')[0]
                    if t2 not in current_tables:
                        target_tables.append(t2)
                    break

            if t in current_tables:
                target_tables = target_tables[1:]
                continue

            raise Exception('Could not autodetect joins')

        # return the actual part of SQL
        join_clause = ''
        for key in current_keys:
            join_left = key[1].split('@')[0]
            join_right = key[2].split('@')[0]

            join_clause += 'LEFT OUTER JOIN {0} ON {1}={2} '.format(key[0], join_left, join_right)

        return join_clause

    def query(self):
        if self._query:
            return self._query

        select_clause = 'SELECT ' + ','.join([prop.full() + ' AS ' + prop.name
                                             for prop in self.properties if not prop.is_generated()]) + ' '

        from_clause = 'FROM {0} '.format(self.user_pk.table)

        # create the join clause
        join_clause = self.join_clause()

        self._query = select_clause + from_clause + join_clause

        # return the `all` query
        return self._query

    def group_by(self):
        result = ' GROUP BY '
        result += ','.join([self.user_pk.connection.primary_key_of(table).split('@')[0] for table in self.group_tables])
        return result

    def all(self, true_id=False):
        # construct query
        query = self.query() + self.group_by()

        # execute query & return results
        return [self.info(row, true_id) for row in self.reduce(self.user_pk.connection.execute(query).fetchall())]

    def filter(self, filters, true_id=False):
        if not filters:
            return self.all()

        if type(filters) in [str, unicode]:
            if filters[0] == '[':
                filters = [f.strip()[1:-1] for f in filters[1:-1].split(' AND ')]

        # create where clause
        if not type(filters) == list:
            filters = filters.replace(' and ', ' AND ').split(' AND ')

        # separate filters between those on simple columns and those on aggregates
        filters_generated = []
        filters_concrete = []
        filters_aggregate = []
        filter_properties = []
        for f in filters:
            # check if the filtered property actually exists & was exposed for filtering
            p_name = re.split('[=<>]', f)[0]
            prop = self.get_property_by_name(p_name)
            if not prop:
                raise PropertyNotFoundException('Property "%s" was not found.' % p_name)
            if not prop.filter_by:
                raise PropertyNotFoundException('Property "%s" was not found.' % prop.name)

            if prop.is_generated():
                filters_generated.append(f)
            elif prop.aggregate is None:
                f = f.replace(prop.name, prop.column)
                filters_concrete.append(f)
                filter_properties.append(prop.name)
            else:
                filters_aggregate.append(f)
                filter_properties.append(prop)
                filter_properties.append(prop.name)

        query = self.query()

        # construct where clause
        if filters_concrete:
            where_clause = 'WHERE ' + ' AND '.join(filters_concrete)
            query += where_clause

        # construct group by clause
        query += self.group_by()

        # aggregate filters must go after the group by in the `having` clause
        if filters_aggregate:
            having_clause = ' HAVING ' + ' AND '.join(filters_aggregate)
            query += having_clause

        # postgres fix
        query = query.replace('"', '\'')

        # execute query & get results
        result = [self.info(row, true_id) for row in self.reduce(self.user_pk.connection.execute(query).fetchall())]

        # filter by generated fields & return result
        return self.filter_by_generated(result, filters_generated)

    def get(self, pk):
        where_clause = 'WHERE {0}={1}'.format(self.user_pk.full(), pk)

        # construct full query
        query = self.query() + where_clause

        # execute query & return results
        return self.info(self.user_pk.connection.execute(query).fetchone())

