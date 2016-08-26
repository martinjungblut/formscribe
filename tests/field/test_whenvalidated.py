import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class WhenValidatedForm(Form):
    class Username(Field):
        key = 'username'

        def validate(self, value):
            if not value:
                raise ValidationError('1')
            StatefulTest.world['username'] = value

    class Gender(Field):
        key = 'gender'

        def validate(self, value):
            if value not in ('male', 'female'):
                raise ValidationError('2')
            StatefulTest.world['gender'] = value

    class Password(Field):
        key = 'password'
        when_validated = ['username', 'gender']

        def validate(self, value):
            StatefulTest.world['password'] = value


class TestWhenValidated(StatefulTest):
    def test_username_not_validated(self):
        data = {
            'gender': 'male',
            'password': 'foo',
            'username': '',
        }
        form = WhenValidatedForm(data=data)
        self.assertEqual(StatefulTest.world['gender'], 'male')
        self.assertEqual(form.errors[0].message, '1')
        self.assertFalse('password' in StatefulTest.world)

    def test_gender_not_validated(self):
        data = {
            'gender': '',
            'password': 'foo',
            'username': 'bar',
        }
        form = WhenValidatedForm(data=data)
        self.assertEqual(StatefulTest.world['username'], 'bar')
        self.assertEqual(form.errors[0].message, '2')
        self.assertFalse('password' in StatefulTest.world)

    def test_validated(self):
        data = {
            'gender': 'female',
            'password': 'foo',
            'username': 'bar',
        }
        form = WhenValidatedForm(data=data)
        self.assertEqual(StatefulTest.world['gender'], 'female')
        self.assertEqual(StatefulTest.world['password'], 'foo')
        self.assertEqual(StatefulTest.world['username'], 'bar')
        self.assertEqual(len(form.errors), 0)
