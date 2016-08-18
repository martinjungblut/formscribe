import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import SubmitError
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class CallableEnabledForm(Form):
    class CallableEnabledField(Field):
        key = 'test-key'

        def enabled(self):
            return StatefulTest.world['is_enabled']

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class PropertyEnabledForm(Form):
    class PropertyEnabledField(Field):
        key = 'test-key'

        @property
        def enabled(self):
            return StatefulTest.world['is_enabled']

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class ClassAttributeEnabledForm(Form):
    class ClassAttributeEnabledField(Field):
        key = 'test-key'
        enabled = False

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class TestFieldInitForm(Form):
    class TestFieldInitField(Field):
        key = 'test-key'

        def __init__(self):
            self.validate_as_int = StatefulTest.world['validate_as_int']

        def validate(self, value):
            if self.validate_as_int:
                try:
                    return int(value)
                except Exception:
                    raise ValidationError(0)
            else:
                try:
                    return value.strip()
                except Exception:
                    raise ValidationError(1)

        def submit(self, value):
            StatefulTest.world['submitted_value'] = value


class WhenValidatedWhenValueForm(Form):
    class ConfirmationCode(Field):
        key = 'confirmation-code'

        def validate(self, value):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError('1')

            StatefulTest.world['confirmation-code'] = True
            return value

        def submit(self, value):
            if value == 2:
                raise SubmitError('2')
            else:
                StatefulTest.world['confirmation-code'] = value

    class Username(Field):
        key = 'username'
        when_validated = ['confirmation-code']

        def validate(self, value):
            StatefulTest.world['username'] = True
            return value

        def submit(self, value):
            StatefulTest.world['username'] = value

    class Password(Field):
        key = 'password'
        when_value = {'username': 'test_username'}

        def validate(self, value):
            StatefulTest.world['password'] = True
            return value

        def submit(self, value):
            StatefulTest.world['password'] = value

    # this field does not implement the submit() method,
    # therefore always raising NotImplementedError
    class CSFRCode(Field):
        key = 'csfr-code'

        def validate(self, value):
            if value != 'csfr-valid':
                raise ValidationError('3')
            return 'csfr-valid'

    def validate(self, confirmationcode, username, password, csfrcode):
        if confirmationcode == 4:
            raise ValidationError('4')

    def submit(self, confirmationcode, username, password, csfrcode):
        if confirmationcode == 5:
            raise SubmitError('5')


class TestWhenValidatedWhenValueForm(StatefulTest):
    def test_get_fields(self):
        form = WhenValidatedWhenValueForm(data={})
        self.assertEqual(form.get_fields(), [
            form.CSFRCode,
            form.ConfirmationCode,
            form.Password,
            form.Username,
        ])

    def test_get_field_dependencies(self):
        form = WhenValidatedWhenValueForm(data={})
        self.assertEqual(form.get_field_dependencies(form.ConfirmationCode),
                         [])
        self.assertEqual(form.get_field_dependencies(form.Username),
                         [form.ConfirmationCode])
        self.assertEqual(form.get_field_dependencies(form.Password),
                         [form.Username])

    def test_valid_no_errors(self):
        data = {'confirmation-code': ' 33 ', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'test_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(StatefulTest.world.get('confirmation-code'), 33)
        self.assertEqual(StatefulTest.world.get('password'), '12345')
        self.assertEqual(StatefulTest.world.get('username'), 'test_username')
        self.assertEqual(len(form.errors), 0)

    def test_invalid_confirmation_code(self):
        # field ValidationError
        data = {'confirmation-code': ' code ', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(isinstance(form.errors[0], ValidationError))
        self.assertEqual(form.errors[0].message, '1')

        # field SubmitError
        data = {'confirmation-code': ' 2 ', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(isinstance(form.errors[0], SubmitError))
        self.assertEqual(form.errors[0].message, '2')

    def test_when_value_correct(self):
        data = {'confirmation-code': '22', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'test_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(StatefulTest.world.get('confirmation-code'), 22)
        self.assertEqual(StatefulTest.world.get('username'), 'test_username')
        self.assertEqual(StatefulTest.world.get('password'), '12345')

    def test_when_value_incorrect(self):
        data = {'confirmation-code': '22', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'another_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(StatefulTest.world.get('confirmation-code'), 22)
        self.assertEqual(StatefulTest.world.get('username'), 'another_username')
        self.assertFalse('password' in StatefulTest.world)

    def test_when_validated_correct(self):
        data = {'confirmation-code': '22', 'csfr-code': 'csfr-valid',
                'username': 'another_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 0)

        self.assertEqual(StatefulTest.world.get('confirmation-code'), 22)
        self.assertEqual(StatefulTest.world.get('username'), 'another_username')

    def test_when_validated_incorrect(self):
        data = {'confirmation-code': 'invalid', 'csfr-code': 'csfr-valid',
                'username': 'another_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '1')
        self.assertTrue('username' not in StatefulTest.world)

    def test_form_validate_unsuccessful(self):
        data = {'confirmation-code': '4', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'test_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '4')

    def test_form_submit_unsuccessful(self):
        data = {'confirmation-code': '5', 'csfr-code': 'csfr-valid',
                'password': '12345', 'username': 'test_username'}
        form = WhenValidatedWhenValueForm(data)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '5')


class TestFieldEnabled(StatefulTest):
    def setUp(self):
        self.world['has_submitted'] = False
        self.world['is_enabled'] = True

    def test_callable_enabled(self):
        CallableEnabledForm({'test-key': True})
        self.assertTrue(self.world['has_submitted'])

        self.world['is_enabled'] = self.world['has_submitted'] = False

        CallableEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])

    def test_property_enabled(self):
        PropertyEnabledForm({'test-key': True})
        self.assertTrue(self.world['has_submitted'])

        self.world['is_enabled'] = self.world['has_submitted'] = False

        PropertyEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])

    def test_class_attribute_enabled(self):
        ClassAttributeEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])


class TestFieldInit(StatefulTest):
    def setUp(self):
        self.world['submitted_value'] = None

    def test_init(self):
        self.world['validate_as_int'] = True
        TestFieldInitForm({'test-key': 3})
        self.assertEqual(self.world['submitted_value'], 3)

        self.world['validate_as_int'] = False
        TestFieldInitForm({'test-key': ' 3 '})
        self.assertEqual(self.world['submitted_value'], '3')


class TestFieldNotImplemented(unittest.TestCase):
    def test_validate_not_implemented(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.validate, None)

    def test_submit_not_implemented(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.submit, None)
