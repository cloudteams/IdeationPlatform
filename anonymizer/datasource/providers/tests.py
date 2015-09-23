from anonymizer.datasource.providers.Dates import age_from_birthday, InvalidBirthday
from anonymizer.datasource.providers.Location import address_to_city, address_to_country, address_to_city_country
from anonymizer.datasource.providers.Ranges import from_int_value, from_float_value, \
    from_int_value__type, from_float_value__type

__author__ = 'dipap'

from django.test import TestCase
from Person import first_name, last_name_initial, male_names, female_names, NoGenderOptions, InvalidGenderOption


class PersonTests(TestCase):

    def test_first_name_is_male(self):
        # kinda based on luck
        for i in range(1, 100):
            name = first_name(('man', 'man', 'woman'))
            self.assertTrue(name in male_names)

    def test_first_name_is_female(self):
        for i in range(1, 100):
            name = first_name(('woman', 'man', 'woman'))
            self.assertTrue(name in female_names)

    def test_first_name_any(self):
        n_of_male = 0
        n_of_female = 0
        for i in range(1, 100):
            name = first_name()
            if name in male_names:
                n_of_male += 1
            elif name in female_names:
                n_of_female += 1
            else:
                raise Exception('Name not male nor female: ' + name)

        # again, must be very unlucky for this test to fail for no reason
        self.assertTrue(n_of_male > 0)
        self.assertTrue(n_of_female > 0)

    def test_no_gender_options(self):
        with self.assertRaises(NoGenderOptions):
            first_name(('Male',))

    def test_invalid_gender_option(self):
        with self.assertRaises(InvalidGenderOption):
            first_name(('Male', 'Man', 'Woman'))

    def test_last_name_initial_format(self):
        surname = last_name_initial()
        self.assertEqual(len(surname), 2)
        self.assertEqual(surname[1], '.')


class RangesTests(TestCase):

    def test_from_value__type(self):
        # test int return type
        tp = from_int_value__type(('1..10|11..20|21..30', 7))
        self.assertEqual(tp, 'Scalar(1..10,11..20,21..30)')

        # test float return type
        tp = from_float_value__type(('1..10|10..20|20..30', 7))
        self.assertEqual(tp, 'Scalar(1..10,10..20,20..30)')

        # test names in scalar type
        tp = from_float_value__type(('1..10=L|10..20=M|20..30=H', 7))
        self.assertEqual(tp, 'Scalar(1..10=L,10..20=M,20..30=H)')

    def test_from_value(self):
        # test simple ranges
        v = from_int_value(('1..10|11..20|21..30', 7))
        self.assertEqual(v, '1..10')

        # test named ranges
        v = from_int_value(('1..10=Low|11..20=Medium|21..30=High', 11))
        self.assertEqual(v, 'Medium')

        # test infinite-sized ranges
        v = from_int_value(('..10=Low|11..20=Medium|21..=High', 56))
        self.assertEqual(v, 'High')

        # test float ranges
        v = from_float_value(('..10=Low|10..20=Medium|20..=High', -4))
        self.assertEqual(v, 'Low')

        v = from_float_value(('..10=Low|10..20=Medium|20..=High', 20))
        self.assertEqual(v, 'High')


class LocationTests(TestCase):

    def test_address_to_city(self):
        self.assertEqual(address_to_city(('Markou Mpotsari 19, Nikea',)), 'Nikea')

    def test_address_to_country(self):
        self.assertEqual(address_to_country(('Markou Mpotsari 19, Nikea',)), 'Greece')

    def test_address_to_city_country(self):
        self.assertEqual(address_to_city_country(('Markou Mpotsari 19, Nikea',)), 'Nikea, Greece')


class DatesTests(TestCase):

    def test_birthday_to_age(self):
        # greater or equal because we don't want the test to fail in a couple of months...
        self.assertGreaterEqual(age_from_birthday(('1991-2-12',)), 24)
        # check that we must pass exactly one argument
        with self.assertRaises(ValueError):
            age_from_birthday(('1991-2-12', 'unexpected'))
        with self.assertRaises(ValueError):
            age_from_birthday(())
        with self.assertRaises(InvalidBirthday):
            age_from_birthday(('undefined',))
