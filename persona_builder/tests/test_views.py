from django.test import TestCase

__author__ = 'dipap'


class PersonaViewTests(TestCase):

    def test_create_persona(self):
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
