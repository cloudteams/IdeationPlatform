__author__ = 'dipap'

from anonymizer.datasource.util import Configuration
from anonymizer.datasource.connections import ConnectionManager
from data import PropertyManager


class UserManagerException(Exception):
    """
    Exceptions caused by the user manager
    """
    pass


class UserManager:
    """
    The User manager is responsible for fetching and filtering user information
    """

    def __init__(self, config_file='', from_str='', token=None):
        if config_file:
            from_str = open(config_file).read()

        self.config = Configuration(from_str=from_str)
        self.cm = ConnectionManager(self.config.get_connection_info())
        self.pm = PropertyManager(self.cm, self.config, token=token)

    def reset_token(self, new_token):
        self.pm.token = new_token

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

    # combine two lists of users, an old and a new version
    # for users in both lists, keep generated information from the old (original) list
    def combine(self, old_list, new_list):
        pk = self.pm.get_primary_key()
        result = []

        for user in new_list:
            found = False

            # try to find user in the old list
            for old_user in old_list:
                if old_user[pk.name] == user[pk.name]:
                    found = True
                    u = user.copy()
                    for prop in self.pm.properties:
                        if prop.is_generated():
                            # check if this property depends on any other that has changes
                            dependencies = self.pm.get_dependencies(prop)
                            dirty = False
                            for dependency in dependencies:
                                if (dependency.name not in old_user) or (dependency.name not in u):
                                    dirty = True
                                    break
                                elif u[dependency.name] != old_user[dependency.name]:
                                    dirty = True
                                    break

                            if not dirty:
                                u[prop.name] = old_user[prop.name]

                    result.append(u)
                    break

            if not found:
                result.append(user)

        return result
