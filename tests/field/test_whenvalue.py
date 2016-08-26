import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class WhenValueForm(Form):
    class Username(Field):
        key = 'username'

        def validate(self, value):
            if not value:
                raise ValidationError('1')

            return value

    class Gender(Field):
        key = 'gender'

        def validate(self, value):
            if value not in ('male', 'female'):
                raise ValidationError('2')

            StatefulTest.world['gender'] = value

            return value

    class Password(Field):
        key = 'password'
        when_value = {'gender': 'male', 'username': 'foo'}

        def validate(self, value):
            StatefulTest.world['password'] = value
            return value


class TestWhenValue(StatefulTest):
    def test_wrong_gender(self):
        data = {
            'gender': 'female',
            'username': 'foo',
            'password': 'somepassword',
        }
        form = WhenValueForm(data=data)
        self.assertEqual(len(form.errors), 0)
        self.assertFalse('password' in StatefulTest.world)

    def test_wrong_username(self):
        data = {
            'gender': 'male',
            'username': 'bar',
            'password': 'somepassword',
        }
        form = WhenValueForm(data=data)
        self.assertEqual(len(form.errors), 0)
        self.assertFalse('password' in StatefulTest.world)

    def test_valid(self):
        data = {
            'gender': 'male',
            'username': 'foo',
            'password': 'somepassword',
        }
        form = WhenValueForm(data=data)
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(StatefulTest.world['password'], 'somepassword')
