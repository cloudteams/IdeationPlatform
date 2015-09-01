from anonymizer.datasource.manager import user_manager, Property, \
    UserManagerException, ProviderNotFound, ProviderMethodNotFound

__author__ = 'dipap'

from django.test import TestCase


class PropertyTests(TestCase):

    def test_load_existing_provider(self):
        Property('^Person.first_name', None)

    def test_exception_on_wrong_provider(self):
        with self.assertRaises(ProviderNotFound):
            Property('^Person_wrong.first_name', None)

    def test_exception_on_wrong_provider_method(self):
        with self.assertRaises(ProviderMethodNotFound):
            Property('^Person.first_name_wrong', None)


class UserManagerTests(TestCase):

    def test_user_exists(self):
        self.assertIsNotNone(user_manager.get(100))

    def test_user_not_exists(self):
        with self.assertRaises(UserManagerException):
            user_manager.get(101)

    def test_single_filter(self):
        res = user_manager.filter('age=37')
        self.assertEqual(len(res), 2)

    def test_multiple_filter(self):
        res = user_manager.filter(['gender="Male"', 'age<35'])
        self.assertEqual(len(res), 18)

    def test_custom_filter(self):
        res = user_manager.filter('age=37 OR gender="Male"')
        self.assertEqual(len(res), 51)

    def test_aggregate_filter(self):
        res = user_manager.filter(['age=37', 'run_duration_avg<13'])
        self.assertEqual(len(res), 1)
