from django.test import TestCase

__author__ = 'dipap'


class PersonaBuilderOAuthTests(TestCase):

    def test_oauth_client(self):
        self.assertIsNotNone(PersonaBuilderOAuthTests())
