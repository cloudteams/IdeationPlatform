from anonymizer.models import ConnectionConfiguration

__author__ = 'dipap'


from django.test import TestCase


class ConnectionViewTests(TestCase):

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
            'path': 'test_site.sqlite3'
        }
        response = self.client.post(form_url, data=data)
        self.assertNotEqual(response.status_code, 400)

        # test that we can't create a connection to a file that does not exist
        data = {
            'path': 'test_site.sqlite31'
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

    def test_select_user_table(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.sqlite3',
                                               info='"name": "test_site.sqlite3"')

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

    def test_select_properties(self):
        ConnectionConfiguration.objects.create(name='test_connection',
                                               connection_type='django.db.backends.sqlite3',
                                               info='"name": "test_site.sqlite3"',
                                               users_table='Users')

        form_url = '/anonymizer/connection/1/select-columns/'

        # test that we can get the form
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 200)
