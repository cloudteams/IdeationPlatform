from anonymizer.datasource.providers.Ranges import from_int_value, from_float_value

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

    def test_from_int_value(self):
        # test simple ranges
        v = from_int_value(('1~10|11~20|21~30', 7))
        self.assertEqual(v, '1~10')

        # test named ranges
        v = from_int_value(('1~10=Low|11~20=Medium|21~30=High', 11))
        self.assertEqual(v, 'Medium')

        # test infinite-sized ranges
        v = from_int_value(('~10=Low|11~20=Medium|21~=High', 56))
        self.assertEqual(v, 'High')

        # test float ranges
        v = from_float_value(('~10=Low|10~20=Medium|20~=High', -4))
        self.assertEqual(v, 'Low')

        v = from_float_value(('~10=Low|10~20=Medium|20~=High', 20))
        self.assertEqual(v, 'High')
