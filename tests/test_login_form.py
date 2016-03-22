"""Login form definition and tests, test FormScribe 0.1 features."""

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
                raise ValidationError('1')

            FormScribeTest.world['confirmation_code'] = True
            return value

        def submit(self, value):
            if not value:
                raise SubmitError('2')
            else:
                FormScribeTest.world['confirmation_code'] = value

    class Username(Field):
        key = 'username'
        when_validated = ['confirmation_code']

        def validate(self, value):
            if not value:
                raise ValidationError('3')

            try:
                value = value.lower().strip()
            except AttributeError:
                raise ValidationError('4')

            FormScribeTest.world['username'] = True
            return value

        def submit(self, value):
            FormScribeTest.world['username'] = value

    class Password(Field):
        key = 'password'
        when_value = {'username': 'test_username'}

        def validate(self, value):
            if not value:
                raise ValidationError('5')

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('6')

            FormScribeTest.world['password'] = True
            return str(value).strip()

        def submit(self, value):
            FormScribeTest.world['password'] = value

    # this field does not implement the submit() method,
    # therefore always raising a NotImplementedError
    class CSFRCode(Field):
        key = 'csfr-code'

        def validate(self, value):
            if value != 'csfr-valid':
                raise ValidationError('13')
            return 'csfr-valid'

    def validate(self, confirmationcode, username, password, csfrcode):
        if confirmationcode and len(str(confirmationcode)) > 16:
            raise ValidationError('7')
        if username and len(username) > 16:
            raise ValidationError('8')
        if password and len(str(password)) > 16:
            raise ValidationError('9')

    def submit(self, confirmationcode, username, password, csfrcode):
        if confirmationcode == 1:
            raise SubmitError('10')
        if username == 'invalid_username':
            raise SubmitError('11')
        if password == '12':
            raise SubmitError('12')


class TestLoginForm(FormScribeTest):
    def test_definition(self):
        form = LoginForm({})
        self.assertEqual(form.get_fields(), [
            form.CSFRCode,
            form.ConfirmationCode,
            form.Password,
            form.Username,
        ])
        self.assertEqual(form.get_field_dependencies(form.ConfirmationCode),
                         [])
        self.assertEqual(form.get_field_dependencies(form.Username),
                         [form.ConfirmationCode])
        self.assertEqual(form.get_field_dependencies(form.Password),
                         [form.Username])

    def test_valid_no_errors(self):
        data = {
            'csfr-code': 'csfr-valid',
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

    def test_invalid_confirmation_code(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': ' code ',
            'password': '12345',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message,
                         '1')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': ' 0 ',
            'password': '12345',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message,
                         '2')

    def test_invalid_username(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '22',
            'password': '12345',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '3')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '22',
            'password': '12345',
            'username': 10,
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '4')

    def test_invalid_password(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '22',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '5')
        self.assertNotEqual(FormScribeTest.world.get('confirmation_code'), 22)
        self.assertNotEqual(FormScribeTest.world.get('username'),
                            'test_username')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '22',
            'password': 'test_password',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '6')
        self.assertNotEqual(FormScribeTest.world.get('confirmation_code'), 22)
        self.assertNotEqual(FormScribeTest.world.get('username'),
                            'test_username')

    def test_when_value(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '22',
            'username': 'another_username',
            'password': '12345',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(FormScribeTest.world.get('confirmation_code'), 22)
        self.assertEqual(FormScribeTest.world.get('username'),
                         'another_username')
        self.assertFalse('password' in FormScribeTest.world)

    def test_when_validated(self):
        data = {
            'csfr-code': 'cfsr-invalid',
            'confirmation_code': 'invalid',
            'username': 'another_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors[0].message, '13')
        self.assertEqual(form.errors[1].message, '1')
        self.assertTrue('username' not in FormScribeTest.world)

        data = {
            'csfr-code': 'cfsr-invalid',
            'confirmation_code': '22',
            'username': 'another_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '13')
        self.assertEqual(FormScribeTest.world.get('confirmation_code'), True)
        self.assertEqual(FormScribeTest.world.get('username'), True)

    def test_form_validation(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '1' * 20,
            'password': '12345',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '7')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '10',
            'password': '12345',
            'username': '1' * 20,
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '8')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '10',
            'password': '1' * 20,
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '9')

    def test_form_submit(self):
        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '1',
            'password': '12345',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '10')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '10',
            'password': '12345',
            'username': 'invalid_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '11')

        data = {
            'csfr-code': 'csfr-valid',
            'confirmation_code': '10',
            'password': '12',
            'username': 'test_username',
        }
        form = LoginForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '12')
