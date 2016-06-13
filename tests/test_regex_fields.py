"""Regex field tests."""

from formscribe import Field
from formscribe import Form
from formscribe import ValidationError
from tests.helpers import FormScribeTest


class ProductManagementForm(Form):
    class ProductName(Field):
        regex_key = 'product-name-(\d+)'
        regex_group = 'products'
        regex_group_key = 'name'

        def validate(self, value):
            try:
                return value.strip()
            except AttributeError:
                raise ValidationError('14')

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
                raise ValidationError('15')

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
            FormScribeTest.world['products'].append({
                'name': product['name'],
                'description': product['description'],
            })


class TestProductManagementForm(FormScribeTest):
    def test_valid(self):
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
            },
            {
                'name': 'second-product-name',
                'description': 'second-product-description',
            },
        ]

        form = ProductManagementForm(data)
        self.assertEqual(len(form.errors), 0)

        for product in FormScribeTest.world['products']:
            self.assertTrue(product in expected)

        for entry in expected:
            self.assertTrue(entry in FormScribeTest.world['products'])

    def test_invalid(self):
        data = {
            'product-name-1': 'first-product-name',
            'product-description-1': 'first-product-description',
            'product-name-2': 'second-product-name',
            'product-description-2': 33,
        }
        form = ProductManagementForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '15')
        self.assertEqual(FormScribeTest.world['products'], [])


class ItemRegexForm(Form):
    class FirstItem(Field):
        regex_group = 'items'
        regex_group_key = 'enabled'
        regex_key = r'item-(\w+)-enabled'

        def validate(self, value):
            return bool(value)

    class SecondItem(Field):
        regex_group = 'items'
        regex_group_key = 'amount'
        regex_key = r'item-(\w+)-amount'

        def validate(self, value):
            return int(value)

    def submit(self, items):
        FormScribeTest.world['items'] = items


class TestMatchRegex(FormScribeTest):
    def test(self):
        data = {
            'item-bar-amount': 5,
            'item-bar-enabled': 1,
            'item-baz-enabled': 1,
            'item-foo-amount': 10,
            'item-foo-enabled': 1,
        }
        expected = [
            {'amount': 10, 'matches': ['foo'], 'enabled': True},
            {'amount': 5, 'matches': ['bar'], 'enabled': True},
            {'matches': ['baz'], 'enabled': True},
        ]

        form = ItemRegexForm(data)
        self.assertEqual(len(form.errors), 0)

        for item in FormScribeTest.world['items']:
            self.assertTrue(item in expected)

        for entry in expected:
            self.assertTrue(entry in FormScribeTest.world['items'])

    def test_no_match(self):
        ItemRegexForm({})
