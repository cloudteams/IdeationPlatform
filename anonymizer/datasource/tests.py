from anonymizer.datasource.manager import user_manager, UserManagerException

__author__ = 'dipap'

from django.test import TestCase


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
