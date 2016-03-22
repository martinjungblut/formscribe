"""Regex field tests."""

from formscribe import Field
from formscribe import Form
from formscribe import ValidationError
from tests.helpers import FormScribeTest


class ProductManagementForm(Form):
    class ProductName(Field):
        regex_key = 'product-name-\d+'
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
        regex_key = 'product-description-\d+'
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
        self.assertEqual(FormScribeTest.world['products'], expected)

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
