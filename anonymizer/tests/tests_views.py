import os

import simplejson as json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.datastructures import MultiValueDictKeyError
from anonymizer.datasource.connections import Connection, ConnectionManager
from anonymizer.models import ConnectionConfiguration

__author__ = 'dipap'


from django.test import TestCase


class ConnectionViewTests(TestCase):

    def test_home_view(self):
        response = self.client.get('/anonymizer/')
        self.assertEqual(response.status_code, 200)

    def test_create_connection(self):
        form_url = '/anonymizer/connection/create/'

        # test that the page is accessible
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can create a mysql connection
        data = {
            'name': 'test_mysql_connection',
            'connection_type': 'django.db.backends.mysql'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 302)

        # test that we can create a sqlite3 connection
        data = {
            'name': 'test_sqlite3_connection',
            'connection_type': 'django.db.backends.sqlite3'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 302)

        # test that we can't create a wrong type connection
        data = {
            'name': 'test_sqlite3_connection',
            'connection_type': 'django.db.backends.sqlite31'
        }
        response = self.client.post(form_url, data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_update_sqlite3_info(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.sqlite3', info='')

        form_url = '/anonymizer/connection/update-info/1/sqlite3/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can't create a connection to the wrong type of file
        data = {
            'path': 'requirements.txt'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 400)

        # test that we can create a connection to the right type of file
        data = {
            'path': 'test-data/test_site.sqlite3'
        }
        response = self.client.post(form_url, data=data)
        self.assertNotEqual(response.status_code, 400)

        # test that we can't create a connection to a file that does not exist
        data = {
            'path': 'test-data/test_site.sqlite31'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_mysql_info(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.mysql', info='')

        form_url = '/anonymizer/connection/update-info/1/mysql/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can create a correct connection
        data = {
            'host': '127.0.0.1',
            'port': '3306',
            'user': 'root',
            'password': '',
            'database': 'test_database'
        }
        response = self.client.post(form_url, data=data)
        self.assertNotEqual(response.status_code, 400)

        # test that we can't create a connection with the wrong password
        data['password'] = '1234'
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_update_postgres_info(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.psycopg2', info='')

        form_url = '/anonymizer/connection/update-info/1/postgres/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can create a correct connection
        data = {
            'host': '127.0.0.1',
            'port': '5432',
            'user': 'postgres',
            'password': '1234',
            'database': 'test_database'
        }
        response = self.client.post(form_url, data=data)
        self.assertNotEqual(response.status_code, 400)

        # test that we can't create a connection with the wrong password
        # travis postgres has no password so we can't test this feature there
        """
        if 'TRAVIS' in os.environ:
            data['password'] = '12345'
            response = self.client.post(form_url, data=data)
            self.assertEqual(response.status_code, 400)
        """

    def test_select_user_table(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.sqlite3',
                                               info='"name": "test-data/test_site.sqlite3"')

        form_url = '/anonymizer/connection/1/suggest-user-table/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can't set wrong the users table
        data = {
            'users_table': 'Users_wrong'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 400)

        # test that we can set the users table
        data = {
            'users_table': 'Users'
        }
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 302)

    def get_test_column_data(self):
        return {
            'form-TOTAL_FORMS': '6',
            'form-INITIAL_FORMS': '6',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-expose': 'on',
            'form-0-name': 'firstname',
            'form-0-c_type': 'varchar(255)',
            'form-0-aggregate': '',
            'form-0-source': '^Person.first_name',
            'form-0-^Person.first_name__param__gender': '@gender',
            'form-0-^Person.first_name__param__male_val': 'Male',
            'form-0-^Person.first_name__param__female_val': 'Female',
            'form-1-expose': 'on',
            'form-1-name': 'lastname',
            'form-1-c_type': 'varchar(255)',
            'form-1-aggregate': '',
            'form-1-source': '^Person.last_name_initial',
            'form-2-expose': 'on',
            'form-2-name': 'gender',
            'form-2-c_type': 'text',
            'form-2-aggregate': '',
            'form-2-source': 'users.gender@test_connection',
            'form-3-expose': 'on',
            'form-3-name': 'age',
            'form-3-c_type': 'mediumint(9)',
            'form-3-aggregate': '',
            'form-3-source': 'users.age@test_connection',
            'form-4-expose': 'on',
            'form-4-name': 'address',
            'form-4-c_type': 'varchar(255)',
            'form-4-aggregate': '',
            'form-4-source': 'users.address@test_connection',
            'form-5-expose': 'on',
            'form-5-name': 'running_duration',
            'form-5-c_type': 'int(11)',
            'form-5-aggregate': 'avg',
            'form-5-source': 'running.duration@test_connection'
        }

    def test_select_properties(self):
        connection_info = '"name":"test_database","user":"root","password":"","host":"127.0.0.1","port":"3306"'
        config = ConnectionConfiguration.objects.create(name='test_connection',
                                                        connection_type='django.db.backends.mysql',
                                                        info=connection_info,
                                                        users_table='users')

        form_url = '/anonymizer/connection/1/select-columns/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # test that we can't post a column with no name
        data = self.get_test_column_data()

        data['form-0-name'] = ''
        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 400)

        # test than we can post to this form
        data = self.get_test_column_data()

        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_setup_standard_connection(self):
        connection_info = '"name":"test_database","user":"root","password":"","host":"127.0.0.1","port":"3306"'
        config = ConnectionConfiguration.objects.create(name='test_connection',
                                                        connection_type='django.db.backends.mysql',
                                                        info=connection_info,
                                                        users_table='users',
                                                        user_pk='users.id@test_connection')

        form_url = '/anonymizer/connection/1/suggest-user-table/'
        response = self.client.post(form_url, data={'users_table': 'users'})
        self.assertEqual(response.status_code, 302)

        form_url = '/anonymizer/connection/1/select-columns/'
        # post column info
        data = self.get_test_column_data()

        response = self.client.post(form_url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_edit_configuration(self):
        self.test_setup_standard_connection()

        # load object after post
        config = ConnectionConfiguration.objects.get(pk=1)

        # assert the correct total json has been created
        """
        expected_config = json.loads(open('test-data/config/mysql_default_config.json').read())
        total_config = json.loads(config.to_json())

        self.assertEqual(expected_config, total_config)
        """

    def test_console(self):
        self.test_setup_standard_connection()

        console_url = '/anonymizer/connection/1/console/'
        query_url = '/anonymizer/connection/1/query/'

        # test the console view responds
        response = self.client.get(console_url)
        self.assertEqual(response.status_code, 200)

        # test the query view returns correct results
        response = self.client.get(query_url + '?q=')
        self.assertEqual(response.status_code, 200)

        # test that the query view expects a ?q argument
        with self.assertRaises(MultiValueDictKeyError):
            self.client.get(query_url)

        # test all command
        response = self.client.get(query_url + '?q=all()')
        self.assertEqual(response.status_code, 200)

        # test help command
        response = self.client.get(query_url + '?q=help')
        self.assertEqual(response.status_code, 200)

        # test filter command
        response = self.client.get(query_url + '?q=filter(running_duration>35)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 4)

        # test malformed query
        response = self.client.get(query_url + '?q=filter(wrong>35)')
        self.assertEqual(response.status_code, 400)

        # test query on generated attributes
        response = self.client.get(query_url + '?q=filter(firstname=Nick)')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(query_url + '?q=filter(firstname="Nick")')
        self.assertEqual(response.status_code, 200)

        # test count query
        response = self.client.get(query_url + '?q=count(gender="Male")')
        self.assertEqual(response.content, '50')

        # test wrong command
        response = self.client.get(query_url + '?q=wrong()')
        self.assertEqual(response.status_code, 400)

    def test_delete_view(self):
        self.test_setup_standard_connection()

        form_url = '/anonymizer/connection/1/delete/'

        # check that we can get the delete form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)

        # check that we can post to the form & the configuration is deleted
        response = self.client.post(form_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConnectionConfiguration.objects.all().count(), 0)

