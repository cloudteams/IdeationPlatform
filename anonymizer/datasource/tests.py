from anonymizer.datasource.managers import Property, \
    UserManagerException, ProviderNotFound, ProviderMethodNotFound, UserManager
from anonymizer.datasource.connections import ConnectionManager, ConnectionNotFound
from anonymizer.datasource.util import Configuration

__author__ = 'dipap'

from django.test import TestCase


class ConnectionManagerTests(TestCase):

    def test_exception_connection_not_found(self):
        config = Configuration('config/sqlite3_config.json')
        cm = ConnectionManager(config.get_connection_info())

        with self.assertRaises(ConnectionNotFound):
            cm.get('wrong_db')

    def test_tables_sqlite3(self):
        # test that there are 3 tables (`Users`, `Running` and the system-specific `sqlite_sequence`)
        config = Configuration('config/sqlite3_config.json')
        tables = ConnectionManager(config.get_connection_info()).get('my_site_db').tables()

        self.assertEqual(len(tables), 3)

    def test_tables_mysql(self):
        # no table must be reported
        config = Configuration('config/mysql_config.json')
        tables = ConnectionManager(config.get_connection_info()).get('my_other_db').tables()

        self.assertEqual(len(tables), 0)


class PropertyTests(TestCase):

    def setUp(self):
        self.um = UserManager('config/sqlite3_config.json')
        super(PropertyTests, self).setUp()

    def test_load_existing_provider(self):
        Property(self.um, '^Person.first_name', None)

    def test_exception_on_wrong_provider(self):
        with self.assertRaises(ProviderNotFound):
            Property(self.um, '^Person_wrong.first_name', None)

    def test_exception_on_wrong_provider_method(self):
        with self.assertRaises(ProviderMethodNotFound):
            Property(self.um, '^Person.first_name_wrong', None)


class UserManagerTests(TestCase):

    def setUp(self):
        self.um = UserManager('config/sqlite3_config.json')
        super(UserManagerTests, self).setUp()

    def test_user_exists(self):
        self.assertIsNotNone(self.um.get(100))

    def test_user_not_exists(self):
        with self.assertRaises(UserManagerException):
            self.um.get(101)

    def test_no_filter(self):
        res = self.um.all()
        self.assertEqual(len(res), 100)

    def test_single_filter(self):
        res = self.um.filter('age=37')
        self.assertEqual(len(res), 2)

    def test_multiple_filter(self):
        res = self.um.filter(['gender="Male"', 'age<35'])
        self.assertEqual(len(res), 18)

    def test_custom_filter(self):
        res = self.um.filter('age=37 OR gender="Male"')
        self.assertEqual(len(res), 51)

    def test_aggregate_filter(self):
        res = self.um.filter(['age=37', 'run_duration_avg<13'])
        self.assertEqual(len(res), 1)
