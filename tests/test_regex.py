"""
The tests located in this module make sure the regex-based capabilities of
FormScribe are working in good condition.

They should always only test regular expression based functionality.
"""

import unittest

from formscribe import Field
from formscribe import Form
from formscribe import ValidationError
from tests.helpers import FormScribeTest


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
                FormScribeTest.world['product_names'].append(value)
            except (KeyError, AttributeError):
                FormScribeTest.world['product_names'] = []
                FormScribeTest.world['product_names'].append(value)

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
                FormScribeTest.world['product_descriptions'].append(value)
            except (KeyError, AttributeError):
                FormScribeTest.world['product_descriptions'] = []
                FormScribeTest.world['product_descriptions'].append(value)

    def validate(self, products):
        FormScribeTest.world['products'] = []

    def submit(self, products):
        for product in products:
            FormScribeTest.world['products'].append(product)


class TestRegularExpressionMatchesAndGrouping(FormScribeTest):
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

        form = MatchingAndGroupingTestForm(data)
        self.assertEqual(len(form.errors), 0)

        for product in FormScribeTest.world['products']:
            self.assertTrue(product in expected)

        for entry in expected:
            self.assertTrue(entry in FormScribeTest.world['products'])

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
        self.assertEqual(FormScribeTest.world['products'], [])

    def test_with_no_data(self):
        """
        This test uses no data at all.
        It merely guarantees that nothing should fail if no regular expression
        match is found.
        """

        MatchingAndGroupingTestForm({})


class KeywordArgsTestForm(Form):
    """
    This form is used to test that a keyword argument will always be provided
    to validate() and submit(), even if there is no match, or if an activation
    condition has not been met.
    
    The argument's value should always be None if it is a 'scalar' argument,
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
        FormScribeTest.world['keyword_args'] = {}
        FormScribeTest.world['keyword_args']['enabled'] = enabled
        FormScribeTest.world['keyword_args']['players'] = players


class TestKeywordArgs(FormScribeTest):
    def test_no_data(self):
        form = KeywordArgsTestForm({})
        self.assertEqual(len(form.errors), 0)

        self.assertEqual(FormScribeTest.world['keyword_args']['enabled'], None)
        self.assertEqual(FormScribeTest.world['keyword_args']['players'], [])

    def test_with_name_but_not_enabled(self):
        form = KeywordArgsTestForm({'enabled': 0, 'player-1-name': 'John'})
        self.assertEqual(len(form.errors), 0)

        self.assertEqual(FormScribeTest.world['keyword_args']['enabled'], False)
        self.assertEqual(FormScribeTest.world['keyword_args']['players'], [])
