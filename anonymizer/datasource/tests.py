from managers.data import Property, ProviderNotFound, ProviderMethodNotFound, PropertyNotFoundException, \
    UnknownOperatorException
from managers.users import UserManagerException, UserManager
from anonymizer.datasource.connections import ConnectionManager, ConnectionNotFound
from anonymizer.datasource.util import Configuration

__author__ = 'dipap'

from django.test import TestCase


class ConnectionTests(TestCase):

    def setUp(self):
        config = Configuration('test-data/config/sqlite3_config.json')
        self.sqlite3 = ConnectionManager(config.get_connection_info()).get('my_site_db')

        config = Configuration('test-data/config/mysql_config.json')
        self.mysql = ConnectionManager(config.get_connection_info()).get('my_other_db')

        config = Configuration('test-data/config/pg_config.json')
        self.pg = ConnectionManager(config.get_connection_info()).get('my_pg_db')

        super(ConnectionTests, self).setUp()

    def test_tables(self):
        # sqlite also reports the system special table
        self.assertEqual(len(self.sqlite3.tables()), 3)
        self.assertEqual(len(self.mysql.tables()), 3)
        self.assertEqual(len(self.pg.tables()), 3)

    def test_table_primary_key(self):
        self.assertEqual(self.sqlite3.primary_key_of('users'), 'users.id@my_site_db')
        self.assertEqual(self.mysql.primary_key_of('users'), 'users.id@my_other_db')
        self.assertEqual(self.pg.primary_key_of('users'), 'users.id@my_pg_db')

    def test_table_properties(self):
        # sqlite falsely reports the id, too
        self.assertEqual(len(self.sqlite3.get_data_properties('Users')[0]), 6)
        self.assertEqual(len(self.mysql.get_data_properties('users')[0]), 5)
        self.assertEqual(len(self.pg.get_data_properties('users')[0]), 5)

        # make sure first element is column name
        self.assertTrue(type(self.sqlite3.get_data_properties('Users')[0][0][0]) in [unicode, str])
        self.assertTrue(type(self.mysql.get_data_properties('users')[0][0][0]) in [unicode, str])
        self.assertTrue(type(self.pg.get_data_properties('users')[0][0][0]) in [unicode, str])

        # also check the properties from other tables pointing to Users as well
        self.assertEqual(len(self.sqlite3.get_data_properties('Users', from_related=True)[0]), 9)
        self.assertEqual(len(self.mysql.get_data_properties('users', from_related=True)[0]), 6)
        self.assertEqual(len(self.pg.get_data_properties('users', from_related=True)[0]), 6)

        # also check other tables pointing to Users as well
        self.assertEqual(len(self.sqlite3.get_data_properties('Running', from_related=True)[0]), 9)
        self.assertEqual(len(self.mysql.get_data_properties('running', from_related=True)[0]), 6)
        self.assertEqual(len(self.pg.get_data_properties('running', from_related=True)[0]), 6)

    def test_related_tables(self):
        self.assertIn('Running', self.sqlite3.get_related_tables('Users')[0])
        self.assertEqual([[u'Running', u'Users.id@my_site_db', u'Running.user@my_site_db']],
                         self.sqlite3.get_related_tables('Users')[1])
        self.assertEqual([[u'running', u'users.id@my_other_db', u'running.user@my_other_db']],
                         self.mysql.get_related_tables('users')[1])
        self.assertEqual([['running', u'users.id@my_pg_db', u'running.user_id@my_pg_db']],
                         self.pg.get_related_tables('users')[1])


class ConnectionManagerTests(TestCase):

    def test_exception_connection_not_found(self):
        config = Configuration('test-data/config/sqlite3_config.json')
        cm = ConnectionManager(config.get_connection_info())

        with self.assertRaises(ConnectionNotFound):
            cm.get('wrong_db')


class PropertyTests(TestCase):

    def setUp(self):
        self.um = UserManager('test-data/config/sqlite3_config.json')
        super(PropertyTests, self).setUp()

    def test_load_existing_provider(self):
        Property(self.um, '^Person.first_name', None)

    def test_exception_on_wrong_provider(self):
        with self.assertRaises(ProviderNotFound):
            Property(self.um, '^Person_wrong.first_name', None)

    def test_exception_on_wrong_provider_method(self):
        with self.assertRaises(ProviderMethodNotFound):
            Property(self.um, '^Person.first_name_wrong', None)

    def test_dynamic_type_with_helper(self):
        p = Property(self.um, '^Ranges.from_float_value(10..20|20..30|30..40, 35)', None, tp='###')
        self.assertEqual(p.tp, 'Scalar(10..20,20..30,30..40)')

    def test_dependencies(self):
        gender = self.um.pm.get_property_by_name('gender')
        first_name = self.um.pm.get_property_by_name('first_name')

        self.assertEqual(self.um.pm.get_dependencies(first_name), [gender])

    def test_exception_on_missing_type_helper(self):
        with self.assertRaises(ProviderMethodNotFound):
            Property(self.um, '^Person.first_name', None, tp='###')

    def test_matches_int(self):
        p = self.um.pm.get_property_by_name('age')

        self.assertTrue(p.matches(5, '=5'))
        self.assertFalse(p.matches(6, '=5'))

        self.assertTrue(p.matches(6, '!=5'))
        self.assertFalse(p.matches(5, '!=5'))

        self.assertTrue(p.matches(4, '<5'))
        self.assertFalse(p.matches(5, '<5'))

        self.assertTrue(p.matches(6, '>5'))
        self.assertFalse(p.matches(5, '>5'))

        self.assertTrue(p.matches(4, '<=5'))
        self.assertTrue(p.matches(5, '<=5'))
        self.assertFalse(p.matches(6, '<=5'))

        self.assertTrue(p.matches(6, '>=5'))
        self.assertTrue(p.matches(5, '>=5'))
        self.assertFalse(p.matches(4, '>=5'))

        # test wrong operator
        with self.assertRaises(UnknownOperatorException):
            self.assertFalse(p.matches(4, '<>5'))

    def test_matches_string(self):
        p = Property(self.um, '^Person.first_name', None)

        self.assertTrue(p.matches('Nick', '=Nick'))
        self.assertFalse(p.matches('Nick', '=John'))

        self.assertFalse(p.matches('Nick', '!=Nick'))
        self.assertTrue(p.matches('Nick', '!=John'))

        # test quoted
        self.assertTrue(p.matches('Nick', '="Nick"'))

    def test_matches_scalar(self):
        p = Property(self.um, '^Ranges.from_float_value(10..20|20..30|30..40, 35)', None, tp='###')

        self.assertTrue(p.matches('10..20', '=10..20'))
        self.assertFalse(p.matches('10..20', '<10..20'))
        self.assertTrue(p.matches('20..30', '>10..20'))
        self.assertTrue(p.matches('20..30', '!=10..20'))

        # test wrong ranges
        with self.assertRaises(ValueError):
            self.assertTrue(p.matches('20..29', '>10..20'))

        with self.assertRaises(ValueError):
            self.assertTrue(p.matches('20..30', '!=10..15'))

    def test_matches_named_scalar(self):
        p = Property(self.um, '^Ranges.from_float_value(10..20=L|20..30=M|30..40=H, 35)', None, tp='###')

        self.assertTrue(p.matches('L', '=L'))
        self.assertFalse(p.matches('L', '<L'))
        self.assertTrue(p.matches('H', '>L'))
        self.assertTrue(p.matches('M', '!=L'))


