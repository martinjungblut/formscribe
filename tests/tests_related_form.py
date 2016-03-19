"""Form tests with field relationships."""

import hashlib
import unittest

from formscribe import Field
from formscribe import Form
from formscribe import SubmitError
from formscribe import ValidationError
from tests.helpers import FormScribeTest


class RelatedForm(Form):
    class FirstPassword(Field):
        key = 'first-password'

        @staticmethod
        def validate(value):
            value = str(value)
            value = value.strip()

            if not value:
                raise ValidationError(0)

            value = hashlib.md5(value.encode('utf-8')).hexdigest()
            return value

    class SecondPassword(Field):
        key = 'second-password'

        @staticmethod
        def validate(value):
            value = str(value)
            value = value.strip()

            if not value:
                raise ValidationError(0)

            value = hashlib.md5(value.encode('utf-8')).hexdigest()
            return value

    @staticmethod
    def validate(firstpassword, secondpassword):
        if firstpassword != secondpassword:
            raise ValidationError(1)
        return firstpassword

    @staticmethod
    def submit(firstpassword, secondpassword):
        FormScribeTest.world['first-password'] = firstpassword


class RelatedFormTest(FormScribeTest):
    def test_definition(self):
        form = RelatedForm({})
        self.assertEqual(form.get_fields(), [
            RelatedForm.FirstPassword,
            RelatedForm.SecondPassword,
        ])

    def test_validation_1(self):
        data = {
            'first-password': 'test_password',
            'second-password': 'test_password',
        }
        form = RelatedForm(data)
        self.assertFalse(form.errors)
        self.assertEqual(FormScribeTest.world['first-password'],
                         '16ec1ebb01fe02ded9b7d5447d3dfc65')

    def test_validation_2(self):
        data = {
            'first-password': 'first_password',
            'second-password': 'second_password',
        }
        form = RelatedForm(data)
        self.assertTrue(form.errors)
        self.assertEqual(form.errors[0].message, 1)
