from django.test import TestCase

from persona_builder.oauth_client import PersonaBuilderOAuthClient

__author__ = 'dipap'


class PersonaBuilderOAuthTests(TestCase):

    def test_oauth_client(self):
        self.assertIsNotNone(PersonaBuilderOAuthClient())
