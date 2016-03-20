"""Bare-bones form tests without field relationships."""

import unittest

from formscribe import Field
from formscribe import Form
from formscribe import SubmitError
from formscribe import ValidationError
from tests.helpers import FormScribeTest


class LoginForm(Form):
    class ConfirmationCode(Field):
        key = 'confirmation_code'

        def validate(self, value):
            try:
                value = value.strip()
            except AttributeError:
                pass

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('Invalid confirmation code.')

            return value

        def submit(self, value):
            FormScribeTest.world['confirmation_code'] = value

    class Username(Field):
        key = 'username'
        when_validated = ['confirmation-code']

        def validate(self, value):
            if not value:
                raise ValidationError('The username is mandatory.')

            try:
                value = value.lower().strip()
            except AttributeError:
                raise ValidationError('The username is invalid.')

            return value

        def submit(self, value):
            FormScribeTest.world['username'] = value

    class Password(Field):
        key = 'password'
        when_value = {'username': 'test_username'}

        def validate(self, value):
            if not value:
                raise ValidationError('The password is mandatory.')

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('The password is invalid.')

            return str(value).strip()

        def submit(self, value):
            FormScribeTest.world['password'] = value


class LoginFormTest(FormScribeTest):
    def test_definition(self):
        form = LoginForm({})
        self.assertEqual(form.get_fields(), [
            form.ConfirmationCode,
            form.Password,
            form.Username,
        ])

    def test_validation_1(self):
        data = {
            'confirmation_code': ' 11 ',
            'username': ' UsErNaMe ',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(FormScribeTest.world.get('confirmation_code'),
                         11)
        self.assertEqual(FormScribeTest.world.get('username'), 'username')

    def test_validation_2(self):
        data = {
            'confirmation_code': ' 22 ',
            'username': ' TEST_UsErNaMe ',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'The password is mandatory.')
        self.assertNotEqual(FormScribeTest.world.get('confirmation_code'),
                            22)
        self.assertNotEqual(FormScribeTest.world.get('username'),
                            'test_username')

    def test_validation_3(self):
        data = {
            'confirmation_code': ' 33 ',
            'password': ' 12345 ',
            'username': ' TEST_UsErNaMe ',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(FormScribeTest.world.get('confirmation_code'),
                         33)
        self.assertEqual(FormScribeTest.world.get('password'), '12345')
        self.assertEqual(FormScribeTest.world.get('username'),
                         'test_username')

