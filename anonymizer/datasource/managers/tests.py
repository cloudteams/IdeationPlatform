from django.test import TestCase
from anonymizer.datasource.connections import ConnectionManager
from anonymizer.datasource.managers.data import PropertyNotFoundException, PropertyManager
from anonymizer.datasource.managers.users import UserManager, UserManagerException
from anonymizer.datasource.util import Configuration

__author__ = 'dipap'


class PropertyManagerTests(TestCase):

    def setUp(self):
        config = Configuration('test-data/config/ctc_config.json')
        ctc_manager = ConnectionManager(config.get_connection_info())
        self.pm = PropertyManager(ctc_manager, config)

    def test_get_all_users(self):
        self.assertEqual(len(self.pm.all()), 19)

    def test_get_female_users(self):
        self.assertEqual(len(self.pm.filter('gender="F"')), 2)

    def test_n_of_walking_users(self):
        self.assertEqual(len(self.pm.filter('activity="Walking"')), 4)


class UserManagerTests(TestCase):

    def setUp(self):
        self.um = UserManager('test-data/config/sqlite3_config.json')
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

    def test_non_exposed_filter(self):
        um = UserManager('test-data/config/sqlite3_config_hide-age.json')
        with self.assertRaises(PropertyNotFoundException):
            um.filter('age=37')
