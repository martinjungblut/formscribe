import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import InvalidFieldError
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class NoRegexGroup(Field):
    """
    Missing the 'regex_group' attribute, InvalidFieldError
    should be raised.
    """

    regex_key = 'some-key'
    regex_group_key = 'some-group-key'

    def validate(self, value):
        return value


class NoRegexGroupKey(Field):
    """
    Missing the 'regex_group_key' attribute, InvalidFieldError
    should be raised.
    """

    regex_key = 'some-key'
    regex_group = 'some-group'

    def validate(self, value):
        return value


class KeywordArgumentsTestForm(Form):
    """
    Form used to test that a keyword argument will always be provided
    to validate() and submit(), even if there is no match, or if an activation
    condition has not been met.

    The argument's value should always be None if it's a scalar argument,
    and it should always be an empty list if it's a regular expression
    based argument.
    """

    class Enabled(Field):
        key = 'enabled'

        def validate(self, value):
            if value is not None:
                return bool(value)

    class Name(Field):
        regex_group = 'players'
        regex_group_key = 'name'
        regex_key = r'player-(\w+)-name'
        when_value = {'enabled': True}

        def validate(self, value):
            return value.strip()

    def submit(self, enabled, players):
        StatefulTest.world['keyword_args'] = {}
        StatefulTest.world['keyword_args']['enabled'] = enabled
        StatefulTest.world['keyword_args']['players'] = players


class MatchingAndGroupingTestForm(Form):
    """Form used to test the basic regular expression funcionality."""

    class ProductName(Field):
        regex_key = 'product-name-(\d+)'
        regex_group = 'products'
        regex_group_key = 'name'

        def validate(self, value):
            try:
                return value.strip()
            except AttributeError:
                raise ValidationError('Name must be a string.')

        def submit(self, value):
            try:
                StatefulTest.world['product_names'].append(value)
            except (KeyError, AttributeError):
                StatefulTest.world['product_names'] = []
                StatefulTest.world['product_names'].append(value)

    class ProductDescription(Field):
        regex_key = 'product-description-(\d+)'
        regex_group = 'products'
        regex_group_key = 'description'

        def validate(self, value):
            try:
                return value.strip()
            except AttributeError:
                raise ValidationError('Description must be a string.')

        def submit(self, value):
            try:
                StatefulTest.world['product_descriptions'].append(value)
            except (KeyError, AttributeError):
                StatefulTest.world['product_descriptions'] = []
                StatefulTest.world['product_descriptions'].append(value)

    def validate(self, products):
        StatefulTest.world['products'] = []

    def submit(self, products):
        for product in products:
            StatefulTest.world['products'].append(product)


class TestRegexFields(unittest.TestCase):
    def test_no_regex_group_invalid_field_error(self):
        self.assertRaises(InvalidFieldError, NoRegexGroup, {})

    def test_no_regex_group_key_invalid_field_error(self):
        self.assertRaises(InvalidFieldError, NoRegexGroupKey, {})


class TestKeywordArguments(StatefulTest):
    def test_with_no_data(self):
        form = KeywordArgumentsTestForm({})
        self.assertEqual(len(form.errors), 0)

        self.assertEqual(StatefulTest.world['keyword_args']['enabled'], None)
        self.assertEqual(StatefulTest.world['keyword_args']['players'], [])

    def test_with_name_but_not_enabled(self):
        form = KeywordArgumentsTestForm({'enabled': 0, 'player-1-name': 'John'})
        self.assertEqual(len(form.errors), 0)

        self.assertEqual(StatefulTest.world['keyword_args']['enabled'], False)
        self.assertEqual(StatefulTest.world['keyword_args']['players'], [])


class TestMatchingAndGrouping(StatefulTest):
    def test_with_valid_data(self):
        data = {
            'product-name-1': 'first-product-name',
            'product-description-1': 'first-product-description',
            'product-name-2': 'second-product-name',
            'product-description-2': 'second-product-description',
        }

        expected = [
            {
                'name': 'first-product-name',
                'description': 'first-product-description',
                'matches': ['1'],
            },
            {
                'name': 'second-product-name',
                'description': 'second-product-description',
                'matches': ['2'],
            },
        ]

        form = MatchingAndGroupingTestForm(data=data)
        self.assertEqual(len(form.errors), 0)

        for product in StatefulTest.world['products']:
            self.assertTrue(product in expected)

        for entry in expected:
            self.assertTrue(entry in StatefulTest.world['products'])

    def test_with_invalid_data(self):
        data = {
            'product-name-1': 'first-product-name',
            'product-description-1': 'first-product-description',
            'product-name-2': 'second-product-name',
            'product-description-2': 33,
        }

        form = MatchingAndGroupingTestForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'Description must be a string.')
        self.assertEqual(StatefulTest.world['products'], [])

    def test_with_no_data(self):
        """
        This test uses no data at all.
        It merely guarantees that nothing should fail if no regular expression
        match is found.
        """

        MatchingAndGroupingTestForm({})
