from formscribe import (Form, Field, ValidationError, SubmitError)
import hashlib
import unittest


class FormCheckerTestCase(unittest.TestCase):
    """
    Base class for all FormChecker TestCases.

    Attributes:
        world (dict): dictionary representing the stateful environment in which
                      Field and Form objects may perform their submit
                      operations.
                      This attribute is reset automatically by
                      setUp() and tearDown().
    """

    world = {}

    def setUp(self):
        FormCheckerTestCase.world = {}

    def tearDown(self):
        FormCheckerTestCase.world = {}


class LoginForm(Form):
    class ConfirmationCode(Field):
        key = 'confirmation_code'

        @staticmethod
        def validate(value):
            try:
                value = value.strip()
            except AttributeError:
                pass

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('Invalid confirmation code.')

            return value

        @staticmethod
        def submit(value):
            FormCheckerTestCase.world['confirmation_code'] = value

    class Username(Field):
        key = 'username'
        when_validated = ['confirmation-code']

        @staticmethod
        def validate(value):
            if not value:
                raise ValidationError('The username is mandatory.')

            try:
                value = value.lower().strip()
            except AttributeError:
                raise ValidationError('The username is invalid.')

            return value

        @staticmethod
        def submit(value):
            FormCheckerTestCase.world['username'] = value

    class Password(Field):
        key = 'password'
        when_value = {'username': 'test_username'}

        @staticmethod
        def validate(value):
            if not value:
                raise ValidationError('The password is mandatory.')

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('The password is invalid.')

            return str(value).strip()

        @staticmethod
        def submit(value):
            FormCheckerTestCase.world['password'] = value


class LoginFormTestCase(FormCheckerTestCase):
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
        self.assertEqual(FormCheckerTestCase.world.get('confirmation_code'),
                         11)
        self.assertEqual(FormCheckerTestCase.world.get('username'), 'username')

    def test_validation_2(self):
        data = {
            'confirmation_code': ' 22 ',
            'username': ' TEST_UsErNaMe ',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'The password is mandatory.')
        self.assertNotEqual(FormCheckerTestCase.world.get('confirmation_code'),
                            22)
        self.assertNotEqual(FormCheckerTestCase.world.get('username'),
                            'test_username')

    def test_validation_3(self):
        data = {
            'confirmation_code': ' 33 ',
            'password': ' 12345 ',
            'username': ' TEST_UsErNaMe ',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(FormCheckerTestCase.world.get('confirmation_code'),
                         33)
        self.assertEqual(FormCheckerTestCase.world.get('password'), '12345')
        self.assertEqual(FormCheckerTestCase.world.get('username'),
                         'test_username')


class InterrelatedForm(Form):
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
        FormCheckerTestCase.world['first-password'] = firstpassword


class InterrelatedFormTestCase(FormCheckerTestCase):
    def test_definition(self):
        form = InterrelatedForm({})
        self.assertEqual(form.get_fields(), [
            InterrelatedForm.FirstPassword,
            InterrelatedForm.SecondPassword,
        ])

    def test_validation_1(self):
        data = {
            'first-password': 'test_password',
            'second-password': 'test_password',
        }
        form = InterrelatedForm(data)
        self.assertFalse(form.errors)
        self.assertEqual(FormCheckerTestCase.world['first-password'],
                         '16ec1ebb01fe02ded9b7d5447d3dfc65')

    def test_validation_2(self):
        data = {
            'first-password': 'first_password',
            'second-password': 'second_password',
        }
        form = InterrelatedForm(data)
        self.assertTrue(form.errors)
        self.assertEqual(form.errors[0].message, 1)
