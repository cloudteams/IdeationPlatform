from anonymizer.datasource.connections import ConnectionManager
from anonymizer.models import ConnectionConfiguration

__author__ = 'dipap'

from django.test import TestCase
from anonymizer.forms import Sqlite3ConnectionForm, MySQLConnectionForm, UserTableSelectionForm


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


# Suggest table tests
class UserTableSelectionFormTests(TestCase):

    def setUp(self):
        config = ConnectionConfiguration.objects.create(name='my_name', connection_type='django.db.backends.sqlite3',
                                                        info='"name": "test_site.sqlite3"')

        # get connection
        manager = ConnectionManager(config.info_to_json())
        self.connection = manager.get(config.name)

        super(UserTableSelectionFormTests, self).setUp()

    def test_table_selection(self):
        f = UserTableSelectionForm(self.connection, data={'users_table': 'Users'})
        self.assertTrue(f.is_valid())

    def test_table_not_exists(self):
        f = UserTableSelectionForm(self.connection, data={'users_table': 'Users_wrong'})
        self.assertFalse(f.is_valid())
