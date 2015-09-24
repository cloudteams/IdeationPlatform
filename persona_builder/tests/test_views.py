from django.test import TestCase
from anonymizer.models import ConnectionConfiguration
from persona_builder.models import Persona

__author__ = 'dipap'


class PersonaViewTests(TestCase):

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

    def create_persona(self):
        data = {
            'name': 'Young runner',
            'description': 'A young person who runs',
        }

        form_url = '/persona-builder/personas/create/'

        # make sure we can't post with a missing avatar
        response = self.client.post(form_url, data=data)
        self.assertTrue('<ul class="errorlist">' in response.content)

        # should be created when we add the avatar
        data['avatar'] = open('test-data/profile.png', 'rb')
        response = self.client.post(form_url, data=data, format='multipart')
        self.assertEqual(response.status_code, 302)

    def test_edit_persona(self):
        self.create_persona()

        form_url = '/persona-builder/personas/1/edit-properties/'

        # test too narrow query
        query = 'age=37'
        response = self.client.post(form_url, data={'query': query})
        self.assertEqual(response.status_code, 400)

        # test correct query
        old_uuid = Persona.objects.get(pk=1).uuid
        query = 'age<30 AND running_duration>10'
        response = self.client.post(form_url, data={'query': query})
        self.assertEqual(response.status_code, 302)
        # test that the uuid has changed with the new query
        new_uuid = Persona.objects.get(pk=1).uuid
        self.assertNotEqual(old_uuid, new_uuid)

        # change that uuid does not change if we post the same query
        old_uuid = new_uuid
        response = self.client.post(form_url, data={'query': query})
        self.assertEqual(response.status_code, 302)
        new_uuid = Persona.objects.get(pk=1).uuid
        self.assertEqual(old_uuid, new_uuid)

        # test persona details view
        response = self.client.get('/persona-builder/personas/1/')
        self.assertEqual(response.status_code, 200)

        # test update users
        connection = ConnectionConfiguration.objects.get(pk=1).get_connection()
        connection.execute("UPDATE users SET gender='Female' WHERE users.id=3;")
        connection.commit()
        users = Persona.objects.get(pk=1).users

        response = self.client.post('/persona-builder/personas/1/update-users/')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(users, Persona.objects.get(pk=1).users)

        connection.execute("UPDATE users SET gender='Male' WHERE users.id=3;")
        connection.commit()

    def test_delete_persona(self):
        self.create_persona()

        response = self.client.post('/persona-builder/personas/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Persona.objects.all().count(), 0)

    def test_personas_list(self):
        response = self.client.get('/persona-builder/personas/')
        self.assertEqual(response.status_code, 200)
