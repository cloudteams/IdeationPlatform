from django.test import TestCase
from anonymizer.models import ConnectionConfiguration
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaBuilderAPITests(TestCase):

    def setUp(self):
        info = """
                "name": "test_database",
                "user": "root",
                "password": "",
                "host": "127.0.0.1",
                "port": "3306"
        """
        properties = open('test-data/config/persona_builder_default_properties.json').read()
        foreign_keys = open('test-data/config/persona_builder_default_foreign_keys.json').read()

        ConnectionConfiguration.objects.create(name='test_connection', connection_type='django.db.backends.mysql',
                                               info=info, user_pk='users.id@test_connection',
                                               users_table='users', properties=properties, foreign_keys=foreign_keys)

    def test_get_info(self):
        self.assertEqual(self.client.get('/persona-builder/api/info/').status_code, 200)

    def test_get_personas(self):
        self.assertEqual(self.client.get('/persona-builder/api/personas/').status_code, 200)

    def test_new_persona(self):
        data = {
            'name': 'Test #1',
            'description': 'This is some test persona'
        }
        response = self.client.post('/persona-builder/api/personas/', data=data)
        self.assertEqual(response.status_code, 201)

        # make sure the Persona has been created
        self.assertEqual(Persona.objects.all().count(), 1)

    def test_get_persona(self):
        data = {
            'name': 'Test #1',
            'description': 'This is some test persona'
        }
        self.client.post('/persona-builder/api/personas/', data=data)

        # get persona #1
        response = self.client.get('/persona-builder/api/persona/1/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)

        # get persona #2 - 404
        response = self.client.get('/persona-builder/api/persona/2/')
        self.assertEqual(response.status_code, 404)

    def test_update_persona(self):
        data = {
            'name': 'Test #1',
            'description': 'This is some test persona'
        }
        self.client.post('/persona-builder/api/personas/', data=data)

        # update
        response = self.client.post('/persona-builder/api/persona/1/', data={'query': 'age>="18..24"'})
        self.assertEqual(response.status_code, 200)

        # make sure the Persona has been updated
        self.assertEqual(Persona.objects.filter(query='age>="18..24"').count(), 1)

    def test_delete_persona(self):
        data = {
            'name': 'Test #1',
            'description': 'This is some test persona'
        }
        self.client.post('/persona-builder/api/personas/', data=data)

        response = self.client.delete('/persona-builder/api/persona/1/')
        self.assertEqual(response.status_code, 204)

        # make sure the Persona has been deleted
        self.assertEqual(Persona.objects.all().count(), 0)

    def test_not_allowed_on_personas_list(self):
        self.assertEqual(self.client.put('/persona-builder/api/info/').status_code, 400)
        self.assertEqual(self.client.delete('/persona-builder/api/info/').status_code, 400)

    def test_not_allowed_on_persona(self):
        data = {
            'name': 'Test #1',
            'description': 'This is some test persona'
        }
        self.client.post('/persona-builder/api/personas/', data=data)
        self.assertEqual(self.client.put('/persona-builder/api/persona/1/').status_code, 400)
