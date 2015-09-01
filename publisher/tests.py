__author__ = 'dipap'

from django.test import TestCase
from publisher.forms import Sqlite3ConnectionForm, MySQLConnectionForm


# sqlite3 form tests
class Sqlite3FormTests(TestCase):

    def test_file_not_exists(self):
        data = {
            'name': 'my_name',
            'path': 'test_site_wrong.sqlite3'
        }

        f = Sqlite3ConnectionForm(data=data)
        self.assertFalse(f.is_valid())

    def test_wrong_file_type(self):
        data = {
            'name': 'my_name',
            'path': 'requirements.txt'
        }

        f = Sqlite3ConnectionForm(data=data)
        self.assertFalse(f.is_valid())

    def test_correct_file_type(self):
        data = {
            'name': 'my_name',
            'path': 'test_site.sqlite3'
        }

        f = Sqlite3ConnectionForm(data=data)
        self.assertTrue(f.is_valid())


# MySQL form tests
class MySQLFormTests(TestCase):

    def get_test_data(self):
        return {
            'name': 'test',
            'host': '127.0.0.1',
            'port': MySQLConnectionForm.DEFAULT_PORT,
            'user': 'root',
            'password': '',
            'database': 'test_database',
        }

    def test_not_existing_connection(self):
        data = self.get_test_data()
        data['database'] = 'wrong_database'

        f = MySQLConnectionForm(data=data)
        self.assertFalse(f.is_valid())

    def test_existing_connection(self):
        f = MySQLConnectionForm(data=self.get_test_data())
        self.assertTrue(f.is_valid())
