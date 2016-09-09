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
        query = "SELECT {0} AS pk FROM {1} WHERE {0}={2}".format(self.pm.user_pk.full(), self.pm.user_pk.table, pk)
        result = self.pm.user_pk.connection.execute(query).fetchall()

        # check uniqueness
        if len(result) == 0:
            raise UserManagerException('User with id={0} does not exist'.format(pk))
        elif len(result) > 1:
            raise UserManagerException('More than one users with id={0} where found'.format(pk))

        return self.pm.get(pk)

    def filter(self, filters, true_id=False, start=None, end=None):
        return self.pm.filter(filters, true_id, start=start, end=end)

    def all(self, start=None, end=None):
        return self.pm.all(start=start, end=end)

    def count(self, filters=None):
        if filters:
            qs = self.pm.filter(filters)
        else:
            qs = self.pm.all()

        return len(qs)

    def list_filters(self, ignore_options=False):
        return self.pm.list_filters(ignore_options)

    def list_properties(self):
        return self.pm.list_properties()

    # combine two users, an old and a new version
    # keep generated information from the old (original) user
    def combine(self, old_user, new_user):
        pk = self.pm.get_primary_key()

        # try to find user in the old list
        if old_user[pk.name] == new_user[pk.name]:
            u = new_user.copy()
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

            return u
        else:
            return new_user
