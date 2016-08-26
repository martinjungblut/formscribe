import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import SubmitError
from formscribe.error import ValidationError


class ErrorsTestForm(Form):
    class Username(Field):
        key = 'username'

        def validate(self, value):
            if value == 'a':
                raise ValidationError('1')
            return value

        def submit(self, value):
            if value == 'b':
                raise SubmitError('2')

    def validate(self, username):
        if username == 'c':
            raise ValidationError('3')

    def submit(self, username):
        if username == 'd':
            raise SubmitError('4')


class TestErrors(unittest.TestCase):
    def test_field_validation_error(self):
        form = ErrorsTestForm(data={'username': 'a'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '1')

    def test_field_submit_error(self):
        form = ErrorsTestForm(data={'username': 'b'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '2')
        
    def test_form_validation_error(self):
        form = ErrorsTestForm(data={'username': 'c'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '3')

    def test_form_submit_error(self):
        form = ErrorsTestForm(data={'username': 'd'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, '4')
